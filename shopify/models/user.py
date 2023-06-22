from odoo import fields,models,api

class UserInherit(models.Model):
    _inherit = 'res.users'

    def get_shops_by_user(self):
        return self.env['shopify.shop'].sudo().search([('user_id', '=', self.id)])