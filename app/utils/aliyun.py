# coding: utf-8
import json
import base64
from flask import current_app
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.request import CommonRequest


class Aliyun():
    def __init__(self):
        pass

    def init_app(self, app):
        self.access_key_id = app.config["ALIYUN_ACCESS_KEY_ID"]
        self.access_key_secret = app.config["ALIYUN_ACCESS_KEY_SECRET"]
        self.location = 'cn-shanghai'
        self.client = AcsClient(self.access_key_id, self.access_key_secret, self.location)

    def send_sms(self, sign_name, template_code, params, phone):
        client = self.client

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', sign_name)
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', json.dumps(params))

        response = client.do_action(request)

        return response
