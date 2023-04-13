import binascii
import os

import shopify
import werkzeug

from odoo import http
from odoo.http import request
import json


class ShopifyController(http.Controller):
    @http.route('/shopify', auth='public')
    def test_link_shopify(self, **kw):
        shopify.Session.setup(api_key='0a5b24655b9809c0cc9912dab9453509', secret='72914fb15c024b423cff071823921bf6')

        shop_url = kw['shop']
        api_version = "2023-01"
        state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        redirect_uri = "https://odoo.website/app"
        scopes = ['read_products', 'read_orders']

        newSession = shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return werkzeug.utils.redirect(auth_url)

    @http.route('/app', auth='public')
    def test_app_shopify(self,**kw):
        shop_url = kw['shop']
        api_version = "2023-01"

        shopify.Session.setup(api_key='0a5b24655b9809c0cc9912dab9453509', secret='72914fb15c024b423cff071823921bf6')
        session = shopify.Session(request.params['shop'], api_version)
        access_token = session.request_token(kw)

        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        shop = shopify.Shop.current()  # Get the current shop
        print(shop.attributes['country'])

        request.env['shopify.shop'].sudo().create({
            'shop_url': shop_url,
            'currency_code' : shop.attributes['currency'],
            'country': shop.attributes['country'],
            'email' : shop.attributes['email'],
            'token' : access_token
        })

        return 'hello'