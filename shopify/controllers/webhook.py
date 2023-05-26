
from odoo import http
import json


class WebhookController(http.Controller):
    @http.route('/webhook/<string:topic>', auth="user")
    def webhook_check(self,topic):
        print(topic)
        return {}
