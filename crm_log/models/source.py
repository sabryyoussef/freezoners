from odoo import fields, models


class Source(models.Model):
    _inherit = "utm.source"

    is_required_referred = fields.Boolean(string="Is Required Referred")
# crm_log/models/crm_stage.py


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    is_hide_quotation_button = fields.Boolean(string="Hide Quotation Button")

