# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    usd_rate = fields.Float(string="USD Rate", compute='_compute_currency_rates', store=False)
    euro_rate = fields.Float(string="Euro Rate", compute='_compute_currency_rates', store=False)
    bank_name = fields.Selection(
        [('nbd', 'EMIRATES NBD'), ('rak', 'RAKBank')],
        string='Bank Name',
        default='nbd'
    )

    def _compute_currency_rates(self):
        usd = self.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
        eur = self.env['res.currency'].sudo().search([('name', '=', 'EUR')], limit=1)
        for rec in self:
            rec.usd_rate = usd.rate
            rec.euro_rate = eur.rate


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    usd_rate = fields.Float(string="USD Rate", compute='_compute_currency_rates', store=False)
    euro_rate = fields.Float(string="Euro Rate", compute='_compute_currency_rates', store=False)
    bank_name = fields.Selection(
        [('nbd', 'EMIRATES NBD'), ('rak', 'RAKBank')],
        string='Bank Name',
        default='nbd'
    )

    def _compute_currency_rates(self):
        usd = self.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
        eur = self.env['res.currency'].sudo().search([('name', '=', 'EUR')], limit=1)
        for rec in self:
            rec.usd_rate = usd.rate
            rec.euro_rate = eur.rate

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'bank_name': self.bank_name,
        })
        return invoice_vals
