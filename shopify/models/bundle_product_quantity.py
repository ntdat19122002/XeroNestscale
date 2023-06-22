from odoo import api, models, fields


class BundleProductQuantity(models.Model):
    _name = 'bundle.product.quantity'

    qty = fields.Integer()
    bundle_id = fields.Many2one('shopify.bundle')
    variant_id = fields.Many2many('shopify.variant','qty_variant_rel')
