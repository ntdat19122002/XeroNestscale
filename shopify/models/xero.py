from odoo import fields, models, api


class XeroShop(models.Model):
    _name = 'xero.shop'

    token = fields.Char()
    user_id = fields.Many2one('res.user')