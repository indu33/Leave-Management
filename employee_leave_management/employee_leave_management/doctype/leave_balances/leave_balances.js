// Copyright (c) 2025, InduSri and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Leave Balances", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Leave Balances', {
    validate: function(frm) {
        // Create a mapping of leave_type to allocated_leaves from leave_records
        let leaveTypeMap = {};
        frm.doc.leave_records.forEach(record => {
            if (record.leave_type) {
                leaveTypeMap[record.leave_type] = record.allocated_leaves || 0;
            }
        });

        // Update remaining_leaves in leave_balance if leaves_taken is empty or zero
        frm.doc.leave_balance.forEach(balance => {
            if ((!balance.leaves_taken || balance.leaves_taken == 0) && leaveTypeMap[balance.leave_type]) {
                balance.remaining_leaves = leaveTypeMap[balance.leave_type];
            } else if (!balance.leaves_taken && leaveTypeMap[balance.leave_type]) {
                balance.remaining_leaves = leaveTypeMap[balance.leave_type];
            }

            // Update balance_leaves_updated_date to today's date if it's empty
            if (!balance.balance_leaves_updated_date) {
                balance.balance_leaves_updated_date = frappe.datetime.get_today();
            }
        });
    }
});


frappe.ui.form.on('Leave Balances', {
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
            fields: ['leave_type']
        },
        callback: function (data) {
            // Clear existing child table data
            frm.clear_table('leave_balance');

            // Loop through the fetched data and append to the child table
            data.message.forEach(function (leave) {
                // Skip "Maternity Leave" if gender is Male
                if (gender === 'Male' && leave.leave_type === 'Maternity Leave') {
                    return;
                }

                frm.add_child('leave_balance', {
                    leave_type: leave.leave_type,
                    
                });
            });

            // Refresh the child table after adding rows
            frm.refresh_field('leave_balance');
        }
    });
};

frappe.ui.form.on('Leave Balances', {
    employee_id: function (frm) {
        if (frm.doc.employee_id) {
            console.log("Employee ID entered:", frm.doc.employee_id); // Debugging
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Leave Allocation',
                    filters: {
                        employee_id: frm.doc.employee_id // Match only employee_id
                    },
                    fields: ['name'] // Fetch the name of the matching record
                },
                callback: function (response) {
                    const leaveAllocations = response.message;
                    console.log("Leave Allocation records found:", leaveAllocations); // Debugging
                    
                    if (leaveAllocations && leaveAllocations.length > 0) {
                        const leaveAllocationName = leaveAllocations[0].name;
                        console.log("Fetching Leave Allocation record:", leaveAllocationName); // Debugging
                        
                        frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                doctype: 'Leave Allocation',
                                name: leaveAllocationName
                            },
                            callback: function (res) {
                                const leaveInfo = res.message.leave_information || [];
                                console.log("Child table data fetched:", leaveInfo); // Debugging

                                if (leaveInfo.length > 0) {
                                    frm.clear_table('leave_records');
                                    leaveInfo.forEach((record) => {
                                        const child = frm.add_child('leave_records');
                                        child.leave_type = record.leave_type;
                                        child.from_date = record.from_date;
                                        child.to_date = record.to_date;
                                        child.allocated_leaves = record.allocated_leaves;
                                    });
                                    frm.refresh_field('leave_records');
                                    frappe.msgprint(__('Leave records have been updated.'));
                                } else {
                                    frappe.msgprint(__('No leave records found in Leave Allocation.'));
                                }
                            }
                        });
                    } else {
                        frappe.msgprint(__('No Leave Allocation record found for this Employee ID.'));
                        frm.clear_table('leave_records');
                        frm.refresh_field('leave_records');
                    }
                }
            });
        }
    }
});


