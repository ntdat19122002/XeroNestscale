from odoo import fields,models,api

class ShopifyShop(models.Model):
    _name = 'shopify.shop'

    user_id = fields.Many2one('res.user')
    shop_url = fields.Char()
    currency_code = fields.Char()
    country = fields.Char()
    email = fields.Char()
    token = fields.Char()

