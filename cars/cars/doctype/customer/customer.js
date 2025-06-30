// Copyright (c) 2025, sarathi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Customer", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Customer', {
 refresh: function(frm) {
 frm.add_custom_button('Create Inspection', () => {
 frappe.new_doc('Inspection Sheet', {
 customer: frm.doc.section_break_njde,
 email: frm.doc.email

 })
 })
 
 }
});

