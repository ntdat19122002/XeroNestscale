from odoo import fields,models,api
from odoo.exceptions import ValidationError


class ShopifyProduct(models.Model):
    _name = 'shopify.bundle'

    shopify_id = fields.Many2one('shopify.shop')
    title = fields.Char()
    description = fields.Char()
    discount_value = fields.Float(default=1)
    discount_type = fields.Selection([('percentage','Percentage'),('fix_amount','Fix Amount')],required=True,default='percentage')
    enable = fields.Boolean(default=True)
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean(default=False)

    qty_ids = fields.One2many('bundle.product.quantity', 'bundle_id')
    setting_id = fields.Many2one('bundle.setting')

    @api.constrains('discount_value')
    def check_discount_value(self):
        try:
            float(self.discount_value)
            if float(self.discount_value) < 0:
                raise ValidationError(_("Discount value must be an int, greater than or equal to 0!"))
        except:
            raise ValidationError(_("Discount value must be an int, greater than or equal to 0!!"))