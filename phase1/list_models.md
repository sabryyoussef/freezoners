# Models Summary

This directory contains the Odoo model definitions for the `phase1` module. Below is a summary of the Python classes defined in these files.

| Class Name | File | Inherits From |
|---|---|---|
| AccountMove | move.py | account.move |
| AccountAnalyticLine | sov.py | account.analytic.line |
| Document | document.py | documents.document |
| Documents | documents.py | documents.document |
| DocumentsShare | documents.py | mail.thread, mail.activity.mixin |
| DocumentsShareWizard | models.py | mail.activity.mixin |
| DocumentRequest | document_request.py | documents.request_wizard |
| MailThread | rating.py | mail.thread |
| Product | product.py | product.product, mail.thread, mail.activity.mixin |
| ProductTemplate | product.py | product.template, mail.thread, mail.activity.mixin |
| Project | project.py | project.project |
| ProjectException | exception.py | mail.thread, mail.activity.mixin |
| ProjectProduct | models.py | mail.thread, mail.activity.mixin |
| ProjectProductRemarks | models.py | mail.thread, mail.activity.mixin |
| ProjectPartnerFields | project_fields.py | mail.thread, mail.activity.mixin, project.project (delegation) |
| ProjectTaskType | task.py | project.task.type |
| Rating | rating.py | rating.rating |
| ResPartner | partner.py | res.partner, mail.thread, mail.activity.mixin |
| SaleOrder | sale.py | sale.order |
| SaleSOV | sov.py | mail.thread, mail.activity.mixin |
| StageTask | project.py | project.task.type |
| Task | task.py | project.task |
| TaskDocumentLines | task_document.py | models.Model |
| TaskDocumentRequiredLines | task_document.py | models.Model | 

# Models Summary

This directory contains the Odoo model definitions for the `phase1` module. Below is a summary of the Python classes defined in these files.

| Class Name | File | Is Inherited |
|---|---|---|
| AccountMove | move.py | True |
| AccountAnalyticLine | sov.py | True |
| Document | document.py | True |
| Documents | documents.py | True |
| DocumentsShare | documents.py | True |
| DocumentsShareWizard | models.py | True |
| DocumentRequest | document_request.py | True |
| MailThread | rating.py | True |
| Product | product.py | True |
| ProductTemplate | product.py | True |
| Project | project.py | True |
| ProjectException | exception.py | True |
| ProjectProduct | models.py | True |
| ProjectProductRemarks | models.py | True |
| ProjectPartnerFields | project_fields.py | True |
| ProjectTaskType | task.py | True |
| Rating | rating.py | True |
| ResPartner | partner.py | True |
| SaleOrder | sale.py | True |
| SaleSOV | sov.py | True |
| StageTask | project.py | True |
| Task | task.py | True |
| TaskDocumentLines | task_document.py | False |
| TaskDocumentRequiredLines | task_document.py | False | 


# Models Summary

This directory contains the Odoo model definitions for the `phase1` module. Below is a summary of the Python classes defined in these files, including their key fields and relationships.

| Class Name | File | Key Fields | Relationships |
|---|---|---|---|
| AccountMove | move.py | `sale_id`, `payment_method`, `project_id`, `task_id`, `payment_status` | Many2one: `sale.order`, `project.project`, `project.task` |
| AccountAnalyticLine | sov.py | `sov_id`, `plan_id`, `amount` | Many2one: `sale.sov`, `account.analytic.plan` |
| Document | document.py | `project_id`, `task_id`, `issue_date`, `type_id`, `partner_id`, `is_verify` | Many2one: `project.project`, `project.task`, `res.partner.document.type`, `res.users`, `res.partner`, `crm.lead`; Many2many: `project.task`, `res.partner` |
| Documents | documents.py | `project_id`, `required_project_id`, `deliverable_project_id`, `type_id`, `partner_id` | Many2one: `project.project`, `res.partner.document.type`, `res.partner`; Many2many: `res.partner` |
| DocumentsShare | documents.py | `name`, `partner_id`, `owner_id`, `folder_id`, `can_upload`, `document_ids` | Many2one: `res.partner`, `res.users`, `documents.folder`, `mail.alias`, `res.users`, `crm.lead`; Many2many: `documents.document`, `documents.tag`, `ir.attachment` |
| DocumentsShareWizard | models.py | `document_share_id`, `summary`, `date_from`, `date_to`, `assigned_to_id` | Many2one: `documents.share`, `res.users`, `mail.activity.type` |
| DocumentRequest | document_request.py | `project_id`, `partner_id`, `type_id`, `deadline`, `request_status` | Many2one: `project.project`, `res.partner`, `res.partner.document.type`; Many2many: `res.partner` |
| MailThread | rating.py | (Abstract Mixin) | Inherited by many models for messaging/activity features. |
| Product | product.py | `partner_ids`, `is_service_commission`, `active_partner_count` | Many2many: `res.partner`; Related: `product.template` |
| ProductTemplate | product.py | `partner_field_ids`, `document_type_ids`, `task_ids`, `is_service_commission` | One2many: `product.res.partner.fields`, `product.template.documents`, `product.template.required.documents`; Many2many: `project.task` |
| Project | project.py | `analytic_account_id`, `sale_id`, `state`, `document_ids`, `partner_id` | Many2one: `account.analytic.account`, `sale.order`, `res.partner`, `account.move`, `res.users`; One2many: `documents.document`, `task.document.lines`, `task.document.required.lines`, `documents.request_wizard`, `res.partner.shareholder`, `project.project.products`; Many2many: `res.partner`, `project.task`, `product.product` |
| ProjectException | exception.py | `name`, `code`, `state`, `severity`, `project_id`, `task_id` | Many2one: `project.project`, `project.task`, `res.users` |
| ProjectProduct | models.py | `product_id`, `project_id`, `partner_id`, `remarks_ids` | Many2one: `product.product`, `project.project`, `res.partner`; Many2many: `project.project.products.remarks` |
| ProjectProductRemarks | models.py | `name`, `product_ids` | Many2many: `project.project.products` |
| ProjectPartnerFields | project_fields.py | `project_id`, `field_id`, `is_required`, `current_value`, `update_value` | Many2one: `project.project`, `ir.model.fields`, `res.country.state`; Related: `res.partner` |
| ProjectTaskType | task.py | `project_ids`, `is_done` | Many2many: `project.project` |
| Rating | rating.py | `rating`, `priority`, `category`, `project_id`, `task_id`, `sale_id` | Many2one: `project.project`, `project.task`, `sale.order`, `res.users`, `ir.model`, `mail.message`, `res.partner` |
| ResPartner | partner.py | `project_product_ids`, `partner_type`, `partner_status`, `document_ids`, `project_ids` | Many2many: `project.project.products`; One2many: `documents.document`, `project.project`; Many2one: `res.partner.license.authority`, `res.country` |
| SaleOrder | sale.py | `state`, `payment_method`, `sov_ids`, `analytic_item_ids`, `partner_id` | One2many: `sale.sov`, `account.move`, `project.project`, `project.task`; Many2many: `account.analytic.line`; Many2one: `res.users`, `res.partner`, `crm.team` |
| SaleSOV | sov.py | `name`, `sale_id`, `project_id`, `revenue`, `planned_expenses`, `product_id` | Many2one: `sale.order`, `project.project`, `res.partner`, `product.product`, `account.analytic.account`; One2many: `account.analytic.line` |
| StageTask | project.py | `is_done` | Inherits from `project.task.type`. (Note: This seems like a small extension of ProjectTaskType) |
| Task | task.py | `project_id`, `stage_id`, `user_ids`, `partner_id`, `document_ids`, `child_ids` | Many2one: `project.project`, `project.task.type`, `account.move`, `sale.order`, `project.task`, `res.partner`; Many2many: `res.partner.document`, `res.users`; One2many: `documents.document`, `task.document.lines`, `task.document.required.lines`, `project.task`, `project.task.checkpoint` |
| TaskDocumentLines | task_document.py | `sequence`, `project_id`, `task_id`, `document_id`, `issue_date`, `expiration_date` | Many2one: `project.project`, `project.task`, `res.partner.document.type`, `res.partner`; Many2many: `ir.attachment` |
| TaskDocumentRequiredLines | task_document.py | `sequence`, `project_id`, `task_id`, `document_id`, `validation_rule`, `expiration_date` | Many2one: `project.project`, `project.task`, `res.partner.document.type`, `res.partner`; Many2many: `ir.attachment` | 

