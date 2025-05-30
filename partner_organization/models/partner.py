from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    parent_partner_ids = fields.Many2many(
        "res.partner",
        relation="parent_partner_ids1",
        column1="parent_partner_ids2",
        column2="parent_partner_ids3",
        string="Parents",
        domain="[('id', '!=', active_id)]"
    )
    parent_chart_ids = fields.Many2many("res.partner", relation="parent_chart_ids1",
                                        column1="parent_chart_ids2", column2="parent_chart_ids3",
                                        string="Parents Chart", compute='get_parent_chart_ids')
    active_id = fields.Integer(string="Active ID", compute="_compute_active_id", store=False, readonly=True)


    def get_parent_chart_ids(self):
        for rec in self:
            partners = self.env['res.partner'].sudo().search(
                [('parent_partner_ids', 'in', rec.id)]).ids
            rec.parent_chart_ids = partners

    @api.onchange('parent_id','parent_partner_ids')
    def change_parent(self):
        for rec in self:
            if rec.parent_partner_ids:
                rec.parent_id = rec.parent_partner_ids[0]
            else:
                rec.parent_id = False

    def _compute_active_id(self):
        for rec in self:
            rec.active_id = rec.id

    # def set_parents(self):
    #     partners = self.env['res.partner'].sudo().search([])
    #     for partner in partners:
    #         if partner.parent_id:
    #             partner.parent_partner_ids = [partner.parent_id.id]

