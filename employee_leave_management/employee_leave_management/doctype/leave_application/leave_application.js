frappe.ui.form.on('Leave Application', {
    onload(frm) {
        // On load, set the status field based on workflow_state
        const workflow_state = frm.doc.workflow_state;
        if (workflow_state && frm.doc.status !== workflow_state) {
            frm.set_value('status', workflow_state);
        }
    },

    refresh(frm) {
        // Check if workflow_state has changed and reload/save the form
        const workflow_state = frm.doc.workflow_state;
        if (workflow_state && frm.doc.status !== workflow_state) {
            frm.set_value('status', workflow_state);
        }
    },

    employee_field_on_change(frm) {
        // Trigger save after employee field is filled out
        if (frm.doc.employee && !frm.doc.__islocal) {
            // Only save if it's not a new document (not local)
            setTimeout(() => {
                frm.save().then(() => {
                    console.log('Form autosaved');
                }).catch((error) => {
                    console.error('Error auto-saving the form:', error);
                });
            }, 2000); // Wait 2 seconds after the employee field is filled
        }
    },

    on_submit(frm) {
        // Ensure status matches workflow_state on submit
        if (frm.doc.workflow_state && frm.doc.status !== frm.doc.workflow_state) {
            frm.set_value('status', frm.doc.workflow_state);
            frm.save();
        }
    },

    gender(frm) {
        update_leave_type_options(frm);
    },

    before_save(frm) {
        const from_date = frm.doc.from_date;
        const to_date = frm.doc.to_date;
        const half_day = frm.doc.half_day;

        if (from_date && to_date) {
            // Calculate the difference in days
            const start = new Date(from_date);
            const end = new Date(to_date);

            let total_days = (end - start) / (1000 * 60 * 60 * 24) + 1; // Add 1 to include the first day
            let total_hours = total_days * 8; // Assuming 8 hours per day

            // Adjust for half-day leave
            if (half_day && total_days === 1) {
                total_hours /= 2; // Half-day applies only for single-day leaves
            }

            // Set the value in the form
            frm.set_value('total_hours', total_hours);

            // Calculate and set the absence field based on total_hours
            let absence_days = Math.round(total_hours / 8); // Round to nearest integer
            frm.set_value('absence', absence_days);
        }
    }
});

function update_leave_type_options(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Leave Type",
            fields: ["name"]
        },
        callback: function (r) {
            if (r.message) {
                const leave_types = r.message.map(lt => lt.name);
                const allowed_leave_types = frm.doc.gender === "Male"
                    ? leave_types.filter(lt => lt !== "Maternity Leave")
                    : leave_types;

                frm.set_query("leave_type", function () {
                    return {
                        filters: [
                            ["Leave Type", "name", "in", allowed_leave_types]
                        ]
                    };
                });
            }
        }
    });
}
