import frappe
from frappe.utils import getdate
from frappe.core.doctype.communication.email import make

def weekly_pending_leaves_summary():
    
    leave_applications = frappe.get_all(
        "Leave Application",
        filters={"status": "Pending for Team Manager"},
        fields=["name", "employee_id", "employee_name", "leave_type", "from_date", "to_date"]
    )

    if not leave_applications:
        frappe.log_error("No pending leave applications found.", "Weekly Pending Leave Summary")
        return

    # Prepare the email content for leave summary
    email_content = format_email_content(leave_applications)
   
    # Send email to Team Manager with pending leave applications
    email_team_manager(email_content)
    
    # Send leave balance updates to employees
    #send_leave_balance_emails()

def format_email_content(leave_applications):
    
    table_headers = """
        <tr>
            <th>Application ID</th>
            <th>Employee ID</th>
            <th>Employee Name</th>
            <th>Leave Type</th>
            <th>From Date</th>
            <th>To Date</th>
            <th>Reason</th>
        </tr>
    """
    table_rows = ""
    for application in leave_applications:
        table_rows += f"""
            <tr>
                <td>{application["name"]}</td>
                <td>{application["employee_id"]}</td>
                <td>{application["employee_name"]}</td>
                <td>{application["leave_type"]}</td>
                <td>{application["from_date"]}</td>
                <td>{application["to_date"]}</td>
            </tr>
        """

    email_body = f"""
        <p>Dear Team Manager,</p>
        <p>Here is the weekly summary of pending leave applications:</p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            {table_headers}
            {table_rows}
        </table>
        <p>Kindly review and take the necessary actions.</p>
        <p>Best regards,<br>Your HR System</p>
    """
    return email_body

def email_team_manager(email_content):
    # Define recipients (Team Manager email)
    recipients = ["janewilliams7f5r@gmail.com"]  # Update with the actual email ID(s)
    
    # Prepare email
    frappe.sendmail(
        recipients=recipients,
        subject="Weekly Summary of Pending Leave Approvals",
        message=email_content,
    )
    frappe.msgprint("Weekly Pending Leave Summary sent to Team Manager.")


def send_leave_balance_emails():
    # Fetch all Leave Balances records
    leave_balances = frappe.get_all(
        'Leave Balances',
        filters={},
        fields=['name', 'employee_id']
    )
    
    # Loop through each Leave Balances record
    for leave_balance in leave_balances:
        employee_id = leave_balance.get('employee_id')
        
        # Check if the employee exists in the Employees doctype
        employee_email = frappe.get_value('Employees', {'employee_id': employee_id}, 'email_address')
        
        if not employee_email:
            frappe.msgprint(f"No email address found for Employee ID: {employee_id}. Skipping.")
            continue
        
        # Fetch the Leave Balances document to access the child table
        leave_balance_doc = frappe.get_doc('Leave Balances', leave_balance['name'])
        leave_details = leave_balance_doc.leave_balance  # Access the child table
        
        # Prepare the email content
        email_content = f"Dear Employee (ID: {employee_id}),\n\nYour Leave Balance:\n\n"
        email_content += "Leave Type\tLeaves Taken\tRemaining Leaves\tLast Updated Date\n"
        email_content += "-" * 60 + "\n"
        
        for leave in leave_details:
            email_content += f"{leave.leave_type}\t{leave.leaves_taken}\t{leave.remaining_leaves}\t{leave.balance_leaves_updated_date or 'N/A'}\n"
        
        email_content += "\nRegards,\nTeam Manager"
        
        # Send the email
        try:
            frappe.sendmail(
                recipients=employee_email,
                subject="Your Monthly Leave Balance Update",
                message=email_content,
                sender="janewilliams7f5r@gmail.com"  # Replace with a valid system email if necessary
            )
            frappe.msgprint(f"Leave balance email sent to {employee_email}")
        except Exception as e:
            frappe.msgprint(f"Failed to send email to {employee_email}: {str(e)}")
