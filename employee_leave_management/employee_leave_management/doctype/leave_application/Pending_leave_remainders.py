import frappe
from frappe.core.doctype.communication.email import make
from datetime import datetime, timedelta

def send_pending_leave_approval_reminders():
    # Get the current date
    today = datetime.today()

    # Fetch all leave applications that are still pending approval
    leave_applications = frappe.get_all(
        "Leave Application",
        filters={"status": "Pending for Team Manager"},
        fields=["name", "employee_id", "leave_type", "employee_name"]
    )

    # Get Team Manager's email
    team_manager_email = frappe.db.get_value("User", {"role_profile_name": "Team Manager"}, "email")

    if not team_manager_email:
        frappe.log_error("No email found for Team Manager role.")
        return

    # Get the Administrator's email
    #administrator_email = frappe.db.get_value("User", {"name": "Administrator"}, "email")
    administrator_email = frappe.db.get_value("User", {"role_profile_name": "Team Lead"}, "email")

    if not administrator_email:
        frappe.log_error("No email found for Administrator.")
        return

    # Send email reminder for each pending leave application
    for leave in leave_applications:
        employee_name = leave.get("employee_name")
        leave_type = leave.get("leave_type")
        
        subject = f"Reminder: Pending Leave Approval for {employee_name}"
        message = f"""
            <p>Dear Team Manager,</p>
            <p>This is a reminder that the following leave application is pending approval:</p>
            <p><strong>Employee:</strong> {employee_name}</p>
            <p><strong>Leave Type:</strong> {leave_type}</p>
            <p>Please review and approve or reject the leave application as soon as possible.</p>
            <p>Best regards,<br>HR Team</p>
        """

        # Send email
        try:
            make(
                recipients=[team_manager_email],
                sender=administrator_email,  # Use Administrator's email as sender
                subject=subject,
                content=message,
                communication_medium="Email",
                send_email=True,
            )
        except Exception as e:
            frappe.log_error(message=str(e), title="Pending Leave Reminder Email Error")