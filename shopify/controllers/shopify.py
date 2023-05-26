import binascii
import os

import shopify
import werkzeug

from odoo import http
from odoo.http import request
import json


class ShopifyController(http.Controller):
    api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
    shopify_key = request.env['ir.config_parameter'].sudo().get_param('shopify_key')
    shopify_secret = request.env['ir.config_parameter'].sudo().get_param('shopify_secret')
    @http.route('/shopify/auth2', auth='public')
    def test_link_shopify(self, **kw):
        shopify.Session.setup(api_key=self.shopify_key, secret=self.shopify_secret)

        shop_url = kw['shop']
        state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        redirect_uri = "https://odoo.website/shopify/callback"
        scopes = [
            "read_products",
            "read_orders",
            "write_orders",
            'read_script_tags',
            'write_script_tags'
        ]

        newSession = shopify.Session(shop_url, self.api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return werkzeug.utils.redirect(auth_url)

    @http.route('/shopify/callback', autgeth="public", type="http", cors="*")
    def test_app_shopify(self,**kw):
        shopify.Session.setup(api_key=self.shopify_key, secret=self.shopify_secret)
        session = shopify.Session(kw['shop'], self.api_version)
        access_token = session.request_token(kw)

        session = shopify.Session(kw['shop'], self.api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        shop = shopify.Shop.current()  # Get the current shop

        if not request.env['shopify.shop'].sudo().search([('shop_url','=',kw['shop'])]):
            self.make_new_shop(shop,access_token)

        self.make_webhook()
        self.make_script_tag()

        return werkzeug.utils.redirect('/apps/shopify?shop='+kw['shop'])

    def make_new_shop(self,shop,access_token):
        if request.env.user:
            request.env['shopify.shop'].sudo().create({
                'shop_url': shop.attributes['domain'],
                'currency_code': shop.attributes['currency'],
                'country': shop.attributes['country'],
                'email': shop.attributes['email'],
                'token': access_token,
                'user_id': request.env.user.id
            })
        else:
            request.env['shopify.shop'].sudo().create({
                'shop_url': shop.attributes['domain'],
                'currency_code': shop.attributes['currency'],
                'country': shop.attributes['country'],
                'email': shop.attributes['email'],
                'token': access_token
            })
    def make_webhook(self):
        shopify.Webhook({
            'topic': "orders/create",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/orders_create",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "orders/update",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/orders_update",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "products/create",
            'address': request.env["ir.config_parameter"].sudo().get_param(
                "ngrok_address") + "/webhook/products_create",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "products/update",
            'address': request.env["ir.config_parameter"].sudo().get_param(
                "ngrok_address") + "/webhook/products_update",
            'format': "json"
        }).save()

    def make_script_tag(self):
        shopify.ScriptTag.create({
            "event": "onload",
            "src": 'https://odoo.website/shopify/static/js/script_tag.js',
            "display_scope": "all",
        })

    # FE UI
    @http.route('/apps/shopify', auth="user", type="http", cors="*")
    def app_shopify_xero(self,**kw):
        if 'shop_url' in request.session:
            print(request.session['shop_url'])
        value = {
            'key': 'value'
        }
        return request.render('shopify.shopify-xero-app', {'app_setting': json.dumps(value)})

    @http.route('/apps/shopify/<string:components>', auth="user", type="http", cors="*")
    def app_shopify_xero_branch(self):
        value = {
            'key': 'value'
        }
        return request.render('shopify.shopify-xero-app', {'app_setting': json.dumps(value)})

    @http.route('/apps/fetch', type='json', auth='user', cors='*', method=['POST'])
    def shopify_fetch_products(self,**kw):
        fetch = []

        for shop in request.env.user.get_shops_by_user():
            session = shopify.Session(shop['shop_url'], self.api_version, shop['token'])
            shopify.ShopifyResource.activate_session(session)

            fetch.append({
                'products': len(shopify.Product.find()),
                'orders':len(shopify.Order.find())
            })
        return json.dumps(fetch)

    # integrate
    @http.route('/api/integrate/ui', auth='user', cors='*', method=['GET'])
    def integrate_shop_ui(self):
        shops = request.env.user.get_shops_by_user()
        shops_data = []
        for shop in shops:
            shops_data.append({
                'name':shop['shop_url']
            })
        return json.dumps(shops_data)

    @http.route('/api/integrate', type='json', auth='user', cors='*', method=['POST'])
    def integrate_shop(self,**kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['url'])])
        if shop:
            if not shop['user_id']:
                shop.write(
                    {
                        'user_id': request.env.user.id
                    }
                )
    @http.route('/api/disintegrate', type='json', auth='user', cors='*', method=['POST'])
    def DisintegateShop(self,**kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['url'])])
        if shop:
            if shop['user_id']:
                shop.sudo().write(
                    {
                        'user_id': False
                    }
                )
