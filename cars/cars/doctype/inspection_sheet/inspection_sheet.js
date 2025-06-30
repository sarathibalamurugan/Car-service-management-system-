// Copyright (c) 2025, sarathi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Inspection Sheet", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Inspection Sheet', {
 refresh: function(frm) {
 frm.add_custom_button('Choose materials', () => {
 frappe.new_doc('Material Request', {
 customer: frm.doc.customer,
    email: frm.doc.email,
    vehicle_number: frm.doc.vehicle_number,
    issues: frm.doc.issues
 })
 })
 
 }
});