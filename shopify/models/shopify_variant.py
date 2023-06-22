from odoo import models,fields

class ShopifyVariant(models.Model):
    _name = 'shopify.variant'

    shopify_id = fields.Char()
    product = fields.Many2one('shopify.product')
    title = fields.Char()
    price = fields.Float()