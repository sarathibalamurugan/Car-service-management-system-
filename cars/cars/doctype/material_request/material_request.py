# Copyright (c) 2025, sarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaterialRequest(Document):
	def before_save(self):
        # Receiver Email ID
		to_email = self.email

		buttons = f"""
            <a href="{frappe.utils.get_url()}/api/method/cars.api.handle_material_request_response?request={self.name}&action=accept"><button>Accept</button></a>
            <a href="{frappe.utils.get_url()}/api/method/cars.api.handle_material_request_response?request={self.name}&action=reject"><button>Reject</button></a>
            <a href="{frappe.utils.get_url()}/api/method/cars.api.handle_material_request_response?request={self.name}&action=revise"><button>Request Revision</button></a>
		"""

        # Get price from Materials Doctype
		material = frappe.get_doc("Materials", self.material_needed)
		amount = material.price + (material.price*(self.profit_percent/100))  # You can also do: material.price * self.count if needed
		

        # Email subject and content
		subject = f"Material invoice for: {self.customer}"
		message = f"""
            <h3>Amount</h3>
            <p><strong>Material:</strong> {self.material_needed}</p>
            <p><strong>Total Amount:</strong> {amount}</p>
			{buttons}
        """

        # Send email
		frappe.sendmail(
			recipients=[to_email],
			subject=subject,
			message=message,
			reference_doctype=self.doctype,
			reference_name=self.name
		)

	def on_submit(self):
		invoice = frappe.get_doc({
		"doctype": "Material Invoice",
		"customer": self.customer,
		"email": self.email,
		"material": self.material_needed,
		"amount": 0
		}).insert(ignore_permissions=True)
		frappe.db.commit()

		frappe.msgprint(f"Invoice Created: {invoice.name}")
