from odoo import api, fields, models, _

class PartnerShareholder(models.Model):
    """
    Partner Shareholder Model
    Links partners to projects as shareholders for compliance purposes
    """
    _name = 'res.partner.shareholder'
    _description = 'Partner Shareholder'

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade',
        help='Project this shareholder is associated with'
    )

    contact_id = fields.Many2one(
        'res.partner',
        string='Shareholder',
        required=True,
        ondelete='cascade',
        help='Partner who is a shareholder'
    )

    share_percentage = fields.Float(
        string='Share Percentage',
        help='Percentage of shares owned by this shareholder'
    )

    is_beneficial_owner = fields.Boolean(
        string='Beneficial Owner',
        default=False,
        help='Indicates if this shareholder is a beneficial owner'
    )

    notes = fields.Text(
        string='Notes',
        help='Additional information about this shareholder'
    )

    _sql_constraints = [
        ('unique_project_contact', 'unique(project_id, contact_id)',
         'A partner can only be a shareholder once per project!')
    ] 