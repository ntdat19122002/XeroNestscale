import json

import werkzeug

from odoo import http

from xero import Xero
from xero.auth import OAuth2Credentials, PublicCredentials
from xero.constants import XeroScopes

my_scope = [XeroScopes.ACCOUNTING_TRANSACTIONS, XeroScopes.PAYROLL_EMPLOYEES]

from odoo.http import request

class XeroController(http.Controller):
    xero_key = request.env['ir.config_parameter'].sudo().get_param('xero_key')
    xero_secret = request.env['ir.config_parameter'].sudo().get_param('xero_secret')
    @http.route('/xero/auth2', type='http', auth='public', cors='*', method=['GET'], csrf=False,)
    def xero_auth(self):
        credentials = OAuth2Credentials(
            self.xero_key, self.xero_secret,callback_uri='https://odoo.website/xero/callback',
            scope=[XeroScopes.OFFLINE_ACCESS, XeroScopes.ACCOUNTING_CONTACTS,
                   XeroScopes.ACCOUNTING_TRANSACTIONS]
        )
        authorization_url = credentials.generate_url()

        request.session['xero_creds'] = credentials.state
        return authorization_url

    @http.route('/xero/callback', type='http', auth='none', cors='*', csrf=False)
    def xero_callback(self,**kw):
        credentials = OAuth2Credentials(**request.session['xero_creds'])
        uri = http.request.httprequest.url.replace('http://','https://')
        print(uri)

        credentials.verify(uri)

        token = credentials.token['access_token']
        print(token)
        shop = request.env['xero.shop'].sudo().search([('user_id', '=', request.env.user.id)])
        if shop:
            shop.sudo().write({
                'token': token
            })
        else:
            request.env['xero.shop'].sudo().create({
                'user_id': request.env.user.id,
                'token': token
            })
        return werkzeug.utils.redirect('https://odoo.website/apps/shopify')

    @http.route('/xero/check_connected', auth='user', cors='*' ,method=['GET'])
    def xero_check(self):
        shop = request.env['xero.shop'].sudo().search([('user_id', '=', request.env.user.id)])
        if shop:
            return json.dumps({'check': True})
        return json.dumps({'check':False})
