from odoo import models,fields

class BundleSetting(models.Model):
    _name = 'bundle.setting'

    bundle_id = fields.Many2one('shopify.bundle')
    location = fields.Selection([('before','Before'),('after','After')])
    font_size = fields.Integer()
    color = fields.Char()
    button_color = fields.Char()