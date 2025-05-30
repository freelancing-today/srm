# Attendance Management System

A full-stack web application for managing employee attendance with an admin dashboard.

## Features

### Employee Features
- Login with employee credentials
- Mark get-in and get-out times
- View daily attendance status
- Real-time clock display

### Admin Features
- Comprehensive dashboard with attendance statistics
- Employee management (Add, Edit, Delete)
- View daily attendance records
- Generate attendance reports and analytics
- Export reports to CSV

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MongoDB
- **Authentication**: Flask-Login
- **Charts**: Chart.js

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd attendance-management-system
```

2. Install dependencies:
```
pip install flask pymongo python-dotenv flask-login
```

3. Configure environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key_here
     MONGO_URI=mongodb+srv://freelancingtodayinfo:<db_password>@cluster0.k6fv5th.mongodb.net/
     DB_PASSWORD=your_mongodb_password_here
     ```

4. Run the application:
```
python app.py
```

5. Access the application:
   - Open your browser and navigate to `http://localhost:5000`
   - Default admin credentials:
     - Username: admin
     - Password: admin123

## Project Structure

```
attendance-management-system/
├── app.py                  # Main application file
├── .env                    # Environment variables
├── static/                 # Static files
│   ├── css/                # CSS files
│   │   └── style.css       # Custom styles
│   └── js/                 # JavaScript files
│       └── main.js         # Custom scripts
└── templates/              # HTML templates
    ├── base.html           # Base template
    ├── login.html          # Login page
    ├── employee_dashboard.html  # Employee dashboard
    ├── admin_dashboard.html     # Admin dashboard
    ├── manage_employees.html    # Employee management
    ├── add_employee.html        # Add employee form
    ├── edit_employee.html       # Edit employee form
    ├── view_attendance.html     # View attendance records
    └── reports.html             # Reports and analytics
```

## Usage

### Employee Workflow
1. Login with employee credentials
2. Mark get-in time at the start of the day
3. Mark get-out time at the end of the day
4. View total hours worked

### Admin Workflow
1. Login with admin credentials
2. View dashboard statistics
3. Manage employees (Add, Edit, Delete)
4. View daily attendance records
5. Generate and export reports

## Security Notes

- Change the default admin password after first login
- Use a strong secret key in the .env file
- Secure your MongoDB connection string and password

## License

[MIT License](LICENSE)