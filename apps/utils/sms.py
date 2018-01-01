# -*- coding: utf-8 -*-

__author__ = 'labike'

import json
import requests


class Sms(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【我的Shop】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict= json.loads(response.text)
        return re_dict


if __name__ == '__main__':
    sms = Sms('5ec95457a78f6b9d354d7b17feb6237d')
    sms.send_sms('2312', '15068775249')