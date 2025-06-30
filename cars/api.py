import frappe
from frappe import _
import time

@frappe.whitelist(allow_guest=True)
def handle_material_request_response(request, action):
    try:
        doc = frappe.get_doc("Material Request", request)

        if action == "accept":
            try:
                doc.db_set("status","accept")
                doc.save(ignore_permissions=True)
                frappe.db.commit()


                invoice = frappe.new_doc("Material Invoice")
                mat=frappe.get_doc("Materials", doc.material_needed)
                mat.db_set("stock_qty",mat.stock_qty - 1)
                
                frappe.sendmail(
                    recipients=[doc.email],
                    subject=f"{doc.customer} - Document PDF",
                    message="Please find the attached document.",
                    attachments=[
                        frappe.attach_print(
                            invoice.doctype,
                            request,
                            file_name=f"{request}",
                        )
                    ],                   
                )

            except Exception as e:
                frappe.log_error(title="Email Sending Error", message=str(e))
                return {"status": "error", "message":e}
            
            

        elif action == "reject":
            doc.db_set("status","reject")
            

        elif action == "revise":
            doc.db_set("status","revise")

            # Notify the creator by email
            creator_email = frappe.db.get_value("User", doc.owner, "email")
            if creator_email:
                material_request_link = f"{frappe.utils.get_url()}/app/material-request/{request}"
                message = f"""
                        <p>The customer has requested a revision for Material Request <b>{request}</b>.</p>
                        <a href="{material_request_link}" style="margin:10px;padding:10px 15px;background:#007bff;color:white;text-decoration:none;border-radius:5px;">
                        Revise Material Request</a>
                    """
                frappe.sendmail(
                    recipients=[creator_email],
                    subject="Revision Requested",
                    message=message,
                    reference_doctype="Material Request",
                    reference_name=request
                )
        else:
            return {"status": "error", "message": "Invalid action"}

        doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Return a minimal response (no UI)
        return ""

    except Exception as e:
        frappe.log_error(title="Material Request API Error", message=str(e))
        return ""
