from odoo import fields,models,api

class FetchHistory(models.Model):
    _name = 'fetch.history'

    shop_id = fields.Many2one('shopify.shop')
    start_date = fields.Date()
    end_date = fields.Date()
    product_number = fields.Integer()
    oder_number = fields.Integer()