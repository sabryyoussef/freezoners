from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class TaskDocumentLines(models.Model):
    """
    Task Document Lines
    Manages document types for tasks
    """
    _name = 'task.document.lines'
    _description = 'Task Document Lines'
    _order = 'sequence, id'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of document in the list'
    )
    
    name = fields.Char(
        string='Name',
        help='Name of the document line'
    )
    
    issue_date = fields.Date(
        string='Issue Date',
        help='Date the document was issued'
    )
    
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade',
        index=True,
        help='Related project'
    )
    
    task_ids = fields.Many2one(
        'project.task',
        string='Task',
        ondelete='cascade',
        index=True,
        help='Related task'
    )
    
    issue_date = fields.Date(
        string='Issue Date',
        help='Date the document was issued'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        help='Attached documents for this line'
    )
    
    document_id = fields.Many2one(
        'res.partner.document.type',
        string='Document Type',
        required=True,
        tracking=True,
        help='Type of document'
    )
    
    is_required = fields.Boolean(
        string='Required',
        default=True,
        tracking=True,
        help='Whether this document is mandatory'
    )
    
    description = fields.Text(
        string='Description',
        help='Additional information about the document requirement'
    )
    
    validity_days = fields.Integer(
        string='Validity (Days)',
        help='Number of days the document remains valid'
    )

    is_required_expiration = fields.Boolean(
        string='Required Expiration',
        help='If true, the expiration date is required'
    )

    expiration_date = fields.Date(
        string='Expiration Date',
        help='Date the document expires'
    )

    is_verify = fields.Boolean(
        string='Verified',
        help='Indicates if the document has been verified'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Related partner for this document line'
    )

    is_moved = fields.Boolean(
        string='Is Moved',
        help='Indicates if the document line has been moved or processed'
    )

    is_ready = fields.Boolean(
        string='Is Ready',
        help='Indicates if the document is ready for processing or verification'
    )

class TaskDocumentRequiredLines(models.Model):
    """
    Task Document Required Lines
    Manages mandatory documents for tasks
    """
    _name = 'task.document.required.lines'
    _description = 'Task Document Required Lines'
    _order = 'sequence, id'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of document in the list'
    )
    
    name = fields.Char(
        string='Name',
        help='Name of the document line'
    )

    task_ids = fields.Many2one(
        "project.task", string="Task", ondelete="cascade"
    )
    document_id = fields.Many2one(
        "documents.document", string="Document", required=True
    )
    issue_date = fields.Date(string="Issue Date")
    
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade',
        index=True,
        help='Related project'
    )
    
    
    
    issue_date = fields.Date(
        string='Issue Date',
        help='Date the document was issued'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        help='Attached documents for this line'
    )
    
    document_id = fields.Many2one(
        'res.partner.document.type',
        string='Document Type',
        required=True,
        tracking=True,
        help='Type of document'
    )
    
    is_required = fields.Boolean(
        string='Required',
        default=True,
        tracking=True,
        help='Whether this document is mandatory'
    )
    
    validation_rule = fields.Selection([
        ('none', 'No Validation'),
        ('expiry', 'Check Expiry'),
        ('completeness', 'Check Completeness'),
        ('both', 'Check Both')
    ], string='Validation Rule',
        default='none',
        tracking=True,
        help='Rule to validate the document'
    )
    
    description = fields.Text(
        string='Description',
        help='Additional information about the document requirement'
    )
    
    validity_days = fields.Integer(
        string='Validity (Days)',
        help='Number of days the document remains valid'
    )

    is_required_expiration = fields.Boolean(
        string='Required Expiration',
        help='If true, the expiration date is required'
    )

    expiration_date = fields.Date(
        string='Expiration Date',
        help='Date the document expires'
    )

    is_verify = fields.Boolean(
        string='Verified',
        help='Indicates if the document has been verified'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Related partner for this document line'
    )

    is_moved = fields.Boolean(
        string='Is Moved',
        help='Indicates if the document line has been moved or processed'
    )

    is_ready = fields.Boolean(
        string='Is Ready',
        help='Indicates if the document is ready for processing or verification'
    )

    def fetch_document(self):
        # Placeholder method - add your logic here
        for record in self:
            _logger.info(f'Fetch Documents button clicked for record {record.id}')
            # Add your logic to fetch documents here
        return True 