from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://freelancingtodayinfo:free123@cluster0.k6fv5th.mongodb.net/your-db?retryWrites=true&w=majority&tls=true')
client = MongoClient(mongo_uri)
db = client['attendance_system']

@app.route('/')
def index():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    employee_count = db.employees.count_documents({})
    today = datetime.now().strftime('%Y-%m-%d')
    present_today = db.attendance.count_documents({'date': today})
    return render_template('admin_dashboard.html', employee_count=employee_count, present_today=present_today)

@app.route('/admin/employees')
def manage_employees():
    employees = list(db.employees.find({}))
    return render_template('manage_employees.html', employees=employees)

@app.route('/admin/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        name = request.form.get('name')
        existing_employee = db.employees.find_one({'employee_id': employee_id})
        if existing_employee:
            flash('Employee ID already exists')
        else:
            db.employees.insert_one({'employee_id': employee_id, 'name': name})
            flash('Employee added successfully')
            return redirect(url_for('manage_employees'))
    return render_template('add_employee.html')

@app.route('/admin/employees/edit/<employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = db.employees.find_one({'_id': ObjectId(employee_id)})
    if not employee:
        flash('Employee not found')
        return redirect(url_for('manage_employees'))
    if request.method == 'POST':
        name = request.form.get('name')
        new_employee_id = request.form.get('employee_id')
        if new_employee_id != employee['employee_id']:
            existing_employee = db.employees.find_one({'employee_id': new_employee_id})
            if existing_employee:
                flash('Employee ID already exists')
                return render_template('edit_employee.html', employee=employee)
        db.employees.update_one({'_id': ObjectId(employee_id)}, {'$set': {'name': name, 'employee_id': new_employee_id}})
        flash('Employee updated successfully')
        return redirect(url_for('manage_employees'))
    return render_template('edit_employee.html', employee=employee)

@app.route('/admin/employees/delete/<employee_id>')
def delete_employee(employee_id):
    db.employees.delete_one({'_id': ObjectId(employee_id)})
    flash('Employee deleted successfully')
    return redirect(url_for('manage_employees'))

@app.route('/admin/attendance')
def view_attendance():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    all_employees = list(db.employees.find({}))
    attendance_records = list(db.attendance.find({'date': date}))
    attendance_dict = {record['employee_id']: record for record in attendance_records}
    combined_records = []
    for employee in all_employees:
        emp_id = employee['employee_id']
        if emp_id in attendance_dict:
            record = attendance_dict[emp_id]
            record['employee_name'] = employee['name']
            # Display times in 12-hour format with correct AM/PM from DB
            def format_time(t, t_type):
                if t:
                    try:
                        dt = datetime.strptime(t, '%H:%M')
                        ampm = t_type if t_type else dt.strftime('%p')
                        return dt.strftime('%I:%M') + f' {ampm}'
                    except Exception:
                        return t
                return ''
            record['in_time'] = format_time(record.get('in_time') or record.get('get_in_time'), record.get('in_time_type'))
            record['out_time'] = format_time(record.get('out_time') or record.get('get_out_time'), record.get('out_time_type'))
            record['hours_worked'] = record.get('hours_worked') or record.get('total_hours') or ''
            combined_records.append(record)
        else:
            combined_records.append({
                'employee_id': emp_id,
                'employee_name': employee['name'],
                'in_time': '',
                'out_time': '',
                'hours_worked': '',
                'status': 'Not Marked',
                '_id': None
            })
    return render_template('view_attendance.html', attendance_records=combined_records, selected_date=date)

@app.route('/admin/attendance/add', methods=['POST'])
def add_attendance():
    employee_id = request.form.get('employee_id')
    date = request.form.get('date')
    in_time = request.form.get('in_time')
    out_time = request.form.get('out_time')
    in_time_type = request.form.get('in_time_type')
    out_time_type = request.form.get('out_time_type')
    # Only use one AM/PM for each time
    def to_24h(t, t_type):
        if t and t_type:
            hour, minute = map(int, t.split(':'))
            if t_type == 'PM' and hour != 12:
                hour += 12
            if t_type == 'AM' and hour == 12:
                hour = 0
            return f"{hour:02d}:{minute:02d}"
        return t
    in_time_24 = to_24h(in_time, in_time_type)
    out_time_24 = to_24h(out_time, out_time_type)
    # Calculate hours worked
    hours_worked = ''
    if in_time_24 and out_time_24:
        try:
            in_dt = datetime.strptime(in_time_24, '%H:%M')
            out_dt = datetime.strptime(out_time_24, '%H:%M')
            if out_dt < in_dt:
                out_dt += timedelta(days=1)
            total_seconds = (out_dt - in_dt).total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            hours_worked = f"{hours}h {minutes}m"
        except Exception:
            flash('Invalid time format')
            return redirect(url_for('view_attendance', date=date))
    # Check if employee exists
    employee = db.employees.find_one({'employee_id': employee_id})
    if not employee:
        flash('Employee not found')
        return redirect(url_for('view_attendance', date=date))
    # Check if attendance record already exists
    existing_record = db.attendance.find_one({'employee_id': employee_id, 'date': date})
    if existing_record:
        db.attendance.update_one(
            {'_id': existing_record['_id']},
            {'$set': {
                'in_time': in_time,
                'out_time': out_time,
                'in_time_type': in_time_type,
                'out_time_type': out_time_type,
                'hours_worked': hours_worked,
                'status': 'Present' if in_time and out_time else 'Incomplete'
            }}
        )
        flash('Attendance record updated successfully')
    else:
        db.attendance.insert_one({
            'employee_id': employee_id,
            'employee_name': employee['name'],
            'date': date,
            'in_time': in_time,
            'out_time': out_time,
            'in_time_type': in_time_type,
            'out_time_type': out_time_type,
            'hours_worked': hours_worked,
            'status': 'Present' if in_time and out_time else 'Incomplete'
        })
        flash('Attendance record added successfully')
    return redirect(url_for('view_attendance', date=date))

@app.route('/admin/attendance/delete/<record_id>')
def delete_attendance(record_id):
    record = db.attendance.find_one({'_id': ObjectId(record_id)})
    if record:
        date = record['date']
        db.attendance.delete_one({'_id': ObjectId(record_id)})
        flash('Attendance record deleted successfully')
    else:
        flash('Record not found')
        date = datetime.now().strftime('%Y-%m-%d')
    
    return redirect(url_for('view_attendance', date=date))

@app.route('/admin/monthly-summary')
def monthly_summary():
    # Get selected month from query or default to current month
    today = datetime.now()
    selected_month = request.args.get('month', today.strftime('%Y-%m'))
    year, month = map(int, selected_month.split('-'))
    # Calculate first and last day of the month
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    start_date = first_day.strftime('%Y-%m-%d')
    end_date = last_day.strftime('%Y-%m-%d')

    # Get all employees
    all_employees = list(db.employees.find({}))
    # Get attendance data for the month
    attendance_data = list(db.attendance.find({
        'date': {'$gte': start_date, '$lte': end_date}
    }))
    # Prepare summary
    summary = []
    for employee in all_employees:
        emp_id = employee['employee_id']
        emp_name = employee['name']
        # Filter attendance records for this employee
        emp_records = [rec for rec in attendance_data if rec['employee_id'] == emp_id and rec.get('status') == 'Present']
        total_minutes = 0
        for rec in emp_records:
            hw = rec.get('hours_worked') or ''
            if 'h' in hw and 'm' in hw:
                try:
                    h = int(hw.split('h')[0])
                    m = int(hw.split('h')[1].strip().split('m')[0])
                    total_minutes += h * 60 + m
                except Exception:
                    pass
        total_hours = total_minutes // 60
        total_mins = total_minutes % 60
        total_hours_str = f"{total_hours}h {total_mins}m"
        total_days = round(total_minutes / (12 * 60), 2)
        summary.append({
            'employee_id': emp_id,
            'name': emp_name,
            'total_hours': total_hours_str,
            'total_days': total_days
        })
    return render_template('monthly_summary.html', summary=summary, selected_month=selected_month)

if __name__ == '__main__':
    app.run(debug=True)
