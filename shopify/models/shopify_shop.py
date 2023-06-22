import shopify

from odoo import fields,models,api

class ShopifyShop(models.Model):
    _name = 'shopify.shop'

    id = fields.Integer()
    user_id = fields.Many2one('res.user')
    shop_url = fields.Char()
    currency_code = fields.Char()
    country = fields.Char()
    email = fields.Char()
    token = fields.Char()

    def fetch_products(self):
        products = shopify.Product.find()
        for product in products:
            product_created = self.env['shopify.product'].sudo().create({
                'shopify_id': self.id,
                'title': product.title,
                'image': product.attributes['image'].attributes['src']
            })
            for variant in product.variants:
                self.env['shopify.variant'].sudo().create({
                    'shopify_id': variant.id,
                    'product': product_created.id,
                    'title':variant.title,
                    'price':variant.price
                })

    def fetch_orders(self):
        orders = shopify.Order.find()
        for order in orders:
            self.env['shopify.product'].sudo().create({
                'shopify_id': self.id,
                'id': orders.id
            })