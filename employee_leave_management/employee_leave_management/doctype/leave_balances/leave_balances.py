import frappe
from frappe.model.document import Document

class LeaveBalances(Document):
    pass

def update_leave_balances(doc, method):
    frappe.logger().debug("Update Leave Balances Triggered")

    # Fetch approved leave applications for the given employee_id
    leave_applications = frappe.get_all(
        "Leave Application",
        filters={"employee_id": doc.employee_id, "status": "Approved"},
        fields=["leave_type", "absence"]
    )
    frappe.logger().debug(f"Leave Applications Found: {leave_applications}")

    # To collect leave types that are not found
    not_found_leave_types = []

    # Check and update the child table for each leave application
    for application in leave_applications:
        leave_type = application.get("leave_type")
        absence = application.get("absence")
        frappe.logger().debug(f"Processing Leave Type: {leave_type}, Absence: {absence}")

        # Check if leave_type exists in the child table
        leave_found = False
        for row in doc.leave_balance:
            if row.leave_type == leave_type:
                # Update leaves_taken with absence value
                frappe.logger().debug(f"Updating leaves_taken for Leave Type: {leave_type}")
                row.leaves_taken = absence  # Corrected field name
                
                # Get the allocated_leaves from the leave_records table
                allocated_leaves = 0
                for leave_record in doc.leave_records:
                    if leave_record.leave_type == leave_type:
                        allocated_leaves = leave_record.allocated_leaves
                        break

                # Ensure both allocated_leaves and leaves_taken are numeric
                try:
                    allocated_leaves = float(allocated_leaves)
                    leaves_taken = float(row.leaves_taken) if row.leaves_taken else 0
                except ValueError:
                    frappe.throw(f"Invalid value for leaves: allocated_leaves={allocated_leaves}, leaves_taken={row.leaves_taken}")

                # Calculate and update remaining_leaves
                row.remaining_leaves = allocated_leaves - leaves_taken

                # Mark the leave as found and break out of the loop
                leave_found = True
                break

        # If leave_type is not found, add to not_found_leave_types
        if not leave_found:
            frappe.logger().debug(f"Leave Type Not Found in Child Table: {leave_type}")
            not_found_leave_types.append(leave_type)

    # Show a message if any leave types are not found
    if not_found_leave_types:
        frappe.msgprint(
            f"The following leave types were not found in the child table: {', '.join(not_found_leave_types)}",
            alert=True
        )
