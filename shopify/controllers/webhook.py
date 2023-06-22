from odoo import http
import json
import shopify
from odoo.http import request


class WebhookController(http.Controller):
    @http.route('/webhook/orders_create',type='json', auth="public")
    def webhook_check(self,**kw):
        print(kw)
        return {}
    @http.route('/webhook/orders_update',type='json', auth="public")
    def webhook_check(self,**kw):
        print(kw)
        return {}
    @http.route('/webhook/products_create',type='json', auth="public")
    def webhook_check(self,**kw):
        print(request.jsonrequest)
        return {}

    @http.route('/webhook/products_update',type='json', auth="public")
    def webhook_check(self,**kw):
        print(request.jsonrequest)
        return {}

