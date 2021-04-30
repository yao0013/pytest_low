# -*- coding: utf-8 -*-
import requests
import pytest
import allure
import string
from core.logs import log
from core.CustomExceptions import *


class ApiHandler(object):
    def __init__(self, api_info):
        self.api_info = api_info
        log.debug(string.Template("api_info: $api_info").substitute(api_info=self.api_info))
        self.method = self.api_info['method']
        self.url = self.api_info['url']
        self.params = self.api_info['params'] if self.api_info['params'] else None
        self.header = self.api_info['header'] if self.api_info['header'] else None

    def api_request(self):
        return self._dispatch()

    def _dispatch(self):
        try:
            method = self.method.lower()
            if method == "get":
                return self.get()
            elif method == "post":
                return self.post()
            elif method == "put":
                return self.put()
            elif method == "delete":
                return self.delete()
            elif method == "patch":
                return self.patch()
            else:
                raise RequestMethodException("api request method not supported")
        except Exception as e:
            log.error(string.Template("api request fail, error info: $e").substitute(e=e))
            raise RequestMethodException("api request fail")

    def get(self):
        res = requests.get(url=self.url, params=self.params, headers=self.header)
        log.debug(string.Template("response json: $res").substitute(res=res.json()))
        return res

    def post(self):
        res = requests.post(self.url, data=self.params, headers=self.header)
        log.debug(string.Template("response json: $res").substitute(res=res.json()))
        return res

    def put(self):
        res = requests.put(self.url, data=self.params, headers=self.header)
        log.debug(string.Template("response json: $res").substitute(res=res.json()))
        return res

    def delete(self):
        res = requests.delete(self.url, data=self.params, headers=self.header)
        log.debug(string.Template("response json: $res").substitute(res=res.json()))
        return res

    def patch(self):
        res = requests.patch(self.url, data=self.params, headers=self.header)
        log.debug(string.Template("response json: $res").substitute(res=res.json()))
        return res


