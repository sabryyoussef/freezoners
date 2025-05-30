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

