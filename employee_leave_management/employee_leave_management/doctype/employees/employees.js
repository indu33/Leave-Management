// Copyright (c) 2025, InduSri and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employees", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Employees', {
	before_save(frm) {
	    let first_name=frm.doc.first_name
	    //let middle_name=frm.doc.middle_name
	    let last_name=frm.doc.last_name
	    full_name=first_name+' '+last_name
	    frm.set_value('full_name',full_name.trim())
	    
		// your code here
	}
})
