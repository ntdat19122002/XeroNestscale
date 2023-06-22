from odoo import fields,models,api

class ShopifyProduct(models.Model):
    _name = 'shopify.product'

    shopify_id = fields.Many2one('shopify.shop')
    id = fields.Char()
    title = fields.Char()
    image = fields.Char()

