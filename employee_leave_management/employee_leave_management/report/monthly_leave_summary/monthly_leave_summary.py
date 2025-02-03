import frappe
from frappe.utils import today, get_first_day, get_last_day

def execute(filters=None):
    # Get the start and end date of the current month
    first_day = get_first_day(today())
    last_day = get_last_day(today())
    
    # Define columns for the report
    columns = [
        {"label": "Employee ID", "fieldname": "employee_id", "fieldtype": "Link", "options": "Employees", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Leave Type", "fieldname": "leave_type", "fieldtype": "Link", "options": "Leave Type", "width": 150},
        {"label": "Absence (Days)", "fieldname": "absence", "fieldtype": "int", "width": 100},
    ]
    
    # Fetch data using Frappe ORM
    leave_applications = frappe.get_all(
        "Leave Application",
        filters={
            "from_date": ["between", [first_day, last_day]],
            "status": "Approved"
        },
        fields=[
            "employee_id",
            "employee_name",
            "leave_type",
            "SUM(absence) as absence",  # Using absence field for the number of days
        ],
        group_by="employee_id, leave_type"
    )
    
    # Prepare data for the report
    data = []
    for leave in leave_applications:
        data.append(leave)
    
    return columns, data