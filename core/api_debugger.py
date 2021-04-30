# -*- coding: utf-8 -*-
"""
api 调试器
"""
import sys
from core.api import ApiHandler
from core.logs import log
from string import Template
from core.case_parse import execute_unit as eut
from core.case_parse.base import Serialize
import json


class Debugger(object):
    def __init__(self, *args, **kwargs):
        self.api_infos = []
        # log.debug(Template("**************$k").substitute(k=kwargs))
        if kwargs.get("file"):
            log.info("处理文件api调试接口")
            self._file_parse(kwargs.get('file'))
        else:
            log.info("处理命令行参数api调试接口")
            self._params_parse(**kwargs)

    def _file_parse(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        try:
            json_conten = json.loads(content)
            log.debug(Template("转换为json格式后的api信息：$api").substitute(api=json_conten))
            log.debug(type(json_conten))
        except Exception as e:
            print("调试文件格式不符合json格式，解析出错，请检查！错误信息: {}".format(str(e)))
            log.error(Template("调试文件格式不符合json格式，解析出错，请检查！错误信息: $e").substitute(e=e))
            sys.exit(-1)
        if isinstance(json_conten, dict):
            if not json_conten.get("url") and not json_conten.get('method'):
                print("调试用例没有url信息或没有method信息")
                log.error(Template("调试用例没有url信息或没有method信息").substitute())
                raise Exception('调试用例没有url信息或没有method信息')
            self.api_infos = [json_conten]
        elif isinstance(json_conten, list):
            for api in json_conten:
                if not api.get("url") and not api.get('method'):
                    print(Template("$api调试用例没有url信息或没有method信息").substitute(api=api))
                    log.error(Template("$api调试用例没有url信息或没有method信息").substitute(api=api))
                    raise Exception(Template("$api调试用例没有url信息或没有method信息").substitute(api=api))
            self.api_infos = json_conten
        else:
            print(Template("调试文件格式不符合json格式，解析结果异常，请检查！解析后的结果：$r").substitute(r=json_conten))
            log.error(Template("调试文件格式不符合json格式，解析结果异常，请检查！解析后的结果：$r").substitute(r=json_conten))
            raise Exception(Template('调试文件格式不符合json格式，解析结果异常，请检查！解析后的结果：$r').substitute(r=json_conten))
        return json_conten

    def _params_parse(self, **kwargs):
        url = kwargs.get('url')
        method = kwargs.get('method')
        params = kwargs.get('params')
        header = kwargs.get('header')
        verify_fields = kwargs.get('verify_fields')
        res_text = kwargs.get('res_text')
        res_header = kwargs.get('res_header')
        status_code = kwargs.get('status_code')
        sql = kwargs.get('sql')
        db_value = kwargs.get('db_value')
        expression = kwargs.get('expression')
        response_time = kwargs.get('response_time')
        dyparam = kwargs.get('dyparam')
        if not url and not method:
            raise Exception('url and method param is require')
        api_info = {
            'url': url,
            'method': method,
            'params': params,
            'header': header,
            'verify_fields': verify_fields,
            'res_text': res_text,
            'res_header': res_header,
            'status_code': status_code,
            'sql': sql,
            'db_value': db_value,
            'expression': expression,
            'response_time': response_time,
            'dyparam': dyparam
        }
        api_info = Serialize(api_info).serialize()
        self.api_infos = [api_info]

    def api_request(self):
        api_infos = self.api_infos
        # log.debug(Template("api_infos: $api").substitute(api=api_infos))
        index = 0
        for api_info in api_infos:
            index += 1
            try:
                log.debug("正在执行用例:{}".format(index))
                res = ApiHandler(api_info).api_request()
            except Exception as e:
                log.error(Template("用例$i 请求异常，异常信息：$e，用例信息：$api").substitute(i=index, e=e, api=api_info))
                continue
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("用例$i 响应结果解析为json格式异常，响应信息：$t，异常信息：$e，用例信息："
                                   "$api").substitute(t=res.text, e=e, api=api_info))
                continue
            flag = True
            if api_info.get("verify_fields"):
                msg = eut.check_verify_fields(api_info["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    # check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if api_info.get("res_text"):
                msg = eut.check_response_text(api_info['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    # check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if api_info.get("res_header"):
                msg = eut.check_response_header(api_info['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    # check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if api_info.get("status_code"):
                msg = eut.check_status_code(api_info['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    # check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if api_info.get("res_time"):
                msg = eut.check_response_time(api_info['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    # check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if api_info.get("expression"):
                msg = eut.check_pyexpression(api_info['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    # check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())

            if not flag:
                log.info(Template("用例$i 执行失败，用例信息：$api").substitute(i=index, api=api_info))





