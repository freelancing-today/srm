// Main JavaScript file for Attendance Management System

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add search functionality to tables
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const value = this.value.toLowerCase();
            const tableId = this.getAttribute('data-table-id') || 'dataTable';
            const table = document.getElementById(tableId);
            
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.indexOf(value) > -1 ? '' : 'none';
                });
            }
        });
    }
    
    // Date range validation for reports
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (startDateInput && endDateInput) {
        endDateInput.addEventListener('change', function() {
            if (startDateInput.value && this.value) {
                const startDate = new Date(startDateInput.value);
                const endDate = new Date(this.value);
                
                if (endDate < startDate) {
                    alert('End date cannot be earlier than start date');
                    this.value = startDateInput.value;
                }
            }
        });
        
        startDateInput.addEventListener('change', function() {
            if (endDateInput.value && this.value) {
                const startDate = new Date(this.value);
                const endDate = new Date(endDateInput.value);
                
                if (endDate < startDate) {
                    endDateInput.value = this.value;
                }
            }
        });
    }
});