# Copyright (c) 2025, sarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseMaterial(Document):
	def before_save(self):
		item = frappe.get_doc("Materials", self.material_name)
		item.stock_qty += self.quantity
		item.save()

