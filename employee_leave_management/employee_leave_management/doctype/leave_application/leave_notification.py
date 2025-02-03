import frappe
from frappe.core.doctype.communication.email import make

def send_leave_notification(doc, method):
    if doc.status not in ["Approved", "Rejected"]:
        return
    employee_email = doc.email  
    
    if not employee_email:
        frappe.log_error(f"No email found for employee: {doc.employee_id}")
        return
    team_manager_email = frappe.db.get_value("User", {"role_profile_name": "Team Manager"}, "email")
    
    if not team_manager_email:
        team_manager_email = frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id")
    
    if not team_manager_email:
        frappe.log_error("No email found for Team Manager role or default outgoing email account.")
        return

    
    leave_balances = frappe.get_list(
        "Leave Balances",
        filters={"parent": doc.employee_id, "leave_type": doc.leave_type},
        fields=["remaining_leaves"],
    )
    remaining_leaves = leave_balances[0].get("remaining_leaves") if leave_balances else "N/A"

   
    subject = f"Leave Application {doc.status}: {doc.leave_type}"
    message = f"""
        <p>Dear {doc.employee_name},</p>
        <p>Your leave application for <strong>{doc.leave_type}</strong> has been <strong>{doc.status}</strong>.</p>
        <p>Best regards,<br>Team Manager</p>
    """

    
    try:
        make(
            recipients=[employee_email],
            sender=team_manager_email,
            subject=subject,
            content=message,
            communication_medium="Email",
            send_email=True,
        )
    except Exception as e:
        frappe.log_error(message=str(e), title="Leave Notification Email Error")
