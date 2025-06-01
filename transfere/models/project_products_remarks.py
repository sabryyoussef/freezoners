from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


from odoo import models, fields



class ProjectProductRemarks(models.Model):
    _name = 'project.project.products.remarks'
    _description = 'Project Product Remarks'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Remark',
        required=True,
        tracking=True
    )
    active = fields.Boolean(
        default=True,
        tracking=True
    )
    product_ids = fields.Many2many(
        'project.project.products',
        string='Products',
        tracking=True
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Remark must be unique!')
    ]
