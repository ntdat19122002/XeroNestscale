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
    def shopify_auth2(self, **kw):
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
    def shopify_callback(self,**kw):
        shopify.Session.setup(api_key=self.shopify_key, secret=self.shopify_secret)
        session = shopify.Session(kw['shop'], self.api_version)
        access_token = session.request_token(kw)

        session = shopify.Session(kw['shop'], self.api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        shopify_shop = shopify.Shop.current()  # Get the current shop

        shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['shop'])])
        if not shop:
            self.make_new_shop(shopify_shop,access_token)
            shop.fetch_products()
            # self.fetch_orders()
        else:
            shop.sudo().write({
                'token':access_token
            })


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
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/products_create",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "products/update",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/products_update",
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
    def app_shopify_fetch(self,**kw):
        fetch = []

        for shop in request.env.user.get_shops_by_user():
            session = shopify.Session(shop['shop_url'], self.api_version, shop['token'])
            shopify.ShopifyResource.activate_session(session)

            start_date = kw['start_date']
            end_date = kw['end_date']
            products_num = len(shopify.Product.find(published_at_min=start_date, published_at_max=end_date))
            orders_num = len(shopify.Order.find(published_at_min=start_date, published_at_max=end_date))

            request.env['fetch.history'].sudo().create({
                'shop_id': shop.id,
                'start_date': kw['start_date'],
                'end_date': kw['end_date'],
                'product_number':products_num,
                'oder_number': orders_num
            })

            fetch.append({
                'products': products_num,
                'orders': orders_num
            })
        return json.dumps(fetch)

    # integrate
    @http.route('/api/integrate/ui', auth='user', cors='*', method=['GET','POST'])
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
    def disintegrate_shop(self,**kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['url'])])
        if shop:
            if shop['user_id']:
                shop.sudo().write(
                    {
                        'user_id': False
                    }
                )

    @http.route('/api/refresh_webhook', type="json", auth='user', cors='*', method=['POST'])
    def refresh_webhook(self, **kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['url'])])
        session = shopify.Session(shop['shop_url'], self.api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        webhooks = shopify.Webhook.find()
        for webhook in webhooks:
            shopify.Webhook.find(webhook.id).destroy()
        self.make_webhook()

    @http.route('/api/refresh_script_tag', type="json", auth='user', cors='*', method=['POST'])
    def refresh_script_tag(self, **kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['url'])])
        session = shopify.Session(shop['shop_url'], self.api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        script_tags = shopify.ScriptTag.find()
        for script_tag in script_tags:
            shopify.ScriptTag.find(script_tag.id).destroy()
        self.make_script_tag()

    @http.route('/products/update', type="json", auth="user", cors='*', method=["POST"])
    def update_product_shopify(self,**kw):
        request.env['shopify.variant'].sudo().search([('product.shopify_id.shop_url', '=', kw['shop'])]).unlink()
        request.env['shopify.product'].sudo().search([('shopify_id.shop_url','=',kw['shop'])]).unlink()

        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['shop'])])
        session = shopify.Session(shop['shop_url'], self.api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        shop.fetch_products()
        return json.dumps(self.return_product_data(kw['shop']))


    @http.route('/products/fetch', type="json", auth="user", cors='*', method=["POST"])
    def fetch_product_shopify(self,**kw):
        return json.dumps(self.return_product_data(kw['shop']))

    def return_product_data(self,shop):
        products = request.env['shopify.product'].sudo().search([('shopify_id.shop_url', '=', shop)])
        products_data = []
        for product in products:
            variants = request.env['shopify.variant'].sudo().search([('product','=',product.id)])
            variants_data = []
            for variant in variants:
                variants_data.append({
                    'id': variant.id,
                    'title':variant.title
                })
            products_data.append({
                'id': product.id,
                'title': product.title,
                'image': product.image,
                'variants':variants_data
            })
        return products_data

    @http.route('/shops/info', type="json", auth='user', cors='*', method=['POST'])
    def return_shop_info(self):
        shops = request.env['shopify.shop'].sudo().search([('user_id','=',request.env.user.id)])
        shops_data = []
        for shop in shops:
            shops_data.append({
                "name" : shop.shop_url
            })
        return json.dumps(shops_data)

    @http.route('/bundle/create', type="json", auth='user', cors='*', method=['POST'])
    def create_bundle(self,**kw):
        print(kw)
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['shop'])])
        bundle = request.env['shopify.bundle'].sudo().create({
            'shopify_id' : shop.id,
            'title':kw['title'],
            'description': kw['description'],
            'discount_type':kw['discount_type'],
            'discount_value':kw['discount_value'],
        })

        for product in kw['products_bundle']:
            request.env['bundle.product.quantity'].sudo().create({
                'qty':product['quantity'],
                'variant_id':[(6,0,product['variant'])],
                'bundle_id':bundle.id
            })

        setting = bundle.setting_id.sudo().create({
            'bundle_id': bundle.id,
            'location':kw['location'],
            'font_size':kw['font_size'],
            'color':kw['color'],
            'button_color':kw['button_color'],
        })

        bundle.setting_id = setting.id

    @http.route('/ui/bundle', type="json", auth='public', cors='*', method=['POST'])
    def show_bundle_in_shopify(self, **kw):
        bundles = request.env['shopify.bundle'].sudo().search([('shopify_id.shop_url','=',kw['shop']),('qty_ids.variant_id.shopify_id','=',kw['variant'])])
        bundle_data = []
        for bundle in bundles:
            variants_data = []
            for qty in bundle.qty_ids:
                for variant in qty.variant_id:
                    variants_data.append({
                        'id': variant.shopify_id,
                        'qty':qty.qty,
                        'image': qty.variant_id.product.image
                    })
            bundle_data.append({
                'title':bundle.title,
                'description':bundle.description,
                'location': bundle.setting_id.location,
                'font_size': bundle.setting_id.font_size,
                'color': bundle.setting_id.color,
                'button_color' : bundle.setting_id.button_color,
                'products': variants_data
            })
        return json.dumps(bundle_data)

