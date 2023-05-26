import werkzeug

import odoo
from odoo import http
import json
import logging
from odoo.addons.portal.controllers.portal import  CustomerPortal
class CustomerPortal(CustomerPortal):

    @odoo.http.route()
    def home(self):
        return werkzeug.utils.redirect('/apps/shopify')

    # @http.route('/my', type='http', auth="user", website=True)
    # def home(self, **kw):
    #     print(1)
    #     return werkzeug.utils.redirect('/shopify/app')