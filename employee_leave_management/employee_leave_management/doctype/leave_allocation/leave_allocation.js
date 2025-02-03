frappe.ui.form.on('Leave Allocation', {
    // Triggered when the form is loaded
    onload: function (frm) {
        populate_leave_information(frm);
    },

    // Triggered when the gender field is changed
    gender: function (frm) {
        populate_leave_information(frm);
    }
});

function populate_leave_information(frm) {
    const gender = frm.doc.gender;

    // Fetch data from the 'Leave Type' doctype
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Leave Type',
            fields: ['leave_type', 'from_date', 'to_date', 'allocated_leaves', 'maximum_carry_forward_leaves']
        },
        callback: function (data) {
            // Clear existing child table data
            frm.clear_table('leave_information');

            // Loop through the fetched data and append to the child table
            data.message.forEach(function (leave) {
                // Skip "Maternity Leave" if gender is Male
                if (gender === 'Male' && leave.leave_type === 'Maternity Leave') {
                    return;
                }

                frm.add_child('leave_information', {
                    leave_type: leave.leave_type,
                    from_date: leave.from_date,
                    to_date: leave.to_date,
                    carry_forward_leaves: leave.maximum_carry_forward_leaves,
                    allocated_leaves: leave.allocated_leaves
                });
            });

            // Refresh the child table after adding rows
            frm.refresh_field('leave_information');
        }
    });
}

