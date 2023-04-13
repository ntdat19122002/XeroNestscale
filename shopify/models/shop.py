from odoo import fields,models,api

class ShopifyShop(models.Model):
    _name = 'shopify.shop'

    shop_url = fields.Char()
    currency_code = fields.Char()
    country = fields.Char()
    email = fields.Char()
    token = fields.Char()