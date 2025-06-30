# Copyright (c) 2025, sarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaterialInvoice(Document):
	def after_insert(self):
		# Calculate the total amount
		material = frappe.get_doc("Materials", self.material)
		percent = frappe.get_doc("Material Request",self.customer)
		self.amount = material.price + (material.price * (percent.profit_percent / 100))

		self.save()
		
		frappe.db.commit()
