import frappe
from frappe.utils import today

def execute(filters=None):
    columns = get_columns()
    data, total_unique_count = get_data()
    
    # Add the total unique count to each row in the "Total Count" column
    for row in data:
        row['total_count'] = total_unique_count
    
    return columns, data

def get_columns():
    return [
        {"label": "Employee ID", "fieldname": "employee_id", "fieldtype": "Data", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "From Date", "fieldname": "from_date", "fieldtype": "Date", "width": 100},
        {"label": "To Date", "fieldname": "to_date", "fieldtype": "Date", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Total Employees Today", "fieldname": "total_count", "fieldtype": "Int", "width": 160},
    ]

def get_data():
    today_date = today()
    leave_applications = frappe.db.sql(
        """
        SELECT 
            employee_id, employee_name, from_date, to_date, status
        FROM 
            `tabLeave Application`
        WHERE 
            DATE(from_date) <= %s AND DATE(to_date) >= %s AND status = 'Approved'
        """,
        (today_date, today_date),
        as_dict=True
    )
    
    # Calculate unique employees on leave
    unique_employees = {entry['employee_id'] for entry in leave_applications}  # Use a set for unique employee IDs
    total_unique_count = len(unique_employees)
    
    return leave_applications, total_unique_count
