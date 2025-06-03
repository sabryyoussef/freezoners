from odoo import api, fields, models

class PartnerStage(models.Model):
    _name = 'partner.stage'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence")

    partner_ids = fields.One2many(
        'res.partner', 'stage_id', string='Partners'
    )
