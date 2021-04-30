# -*- coding: utf-8 -*-
"""
功能：通过脚本自动生成的初始化测试套用例
"""
import os
import pytest
import allure
import pytz
import time
from string import Template
from datetime import datetime
from core.logs import CustomLogger
import pytest_check as check
from core.api import ApiHandler
from core.case_parse.execute_unit import VarReplace, parse_interface_var, parse_case_vars, var_add_random_str, datetime_translate
from core.case_parse import execute_unit as eut
from core.case_parse.base import Process
from core.results import RS


current_time = str(datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S"))
file_name = os.path.basename(__file__).rstrip('.py')
log_name = "{}_{}.log".format(file_name, current_time)
log = CustomLogger(filename=log_name).logger


class CommonInterfaceVars(object):
    def __init__(self):
        self.interface_vars = Process.global_vars
        self.backup_vars = {}


init_object = CommonInterfaceVars()


class TestInitDatas(object):

    @pytest.mark.run(order=10001)
    def test_用户登录获取token(self):
        test_case = {'order': 10001, 'module': '用户登录', 'casename': '用户登录获取token', 'description': '云主机服务-资源管理-弹性计算-映像管理-导入映像', 'url': 'http://192.168.203.83/api/portal/identity/user/login.sso', 'method': 'POST', 'params': {'loginName': '{username}', 'password': '{password}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, 'case_vars': '', 'interface_var': {'token': 'token'}, 'wait_time': '', 'hostname': 'http://192.168.203.83'}
        log.info(Template("task_init 正在执行：$name用例").substitute(name=test_case['casename']))

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, init_object)
        test_case = VarReplace(test_case, [init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            res = ApiHandler(api_info).api_request() #发送请求，返回响应
        except Exception as e:
            log.error(Template("task_init api request fail,error info: $e").substitute(e=e))
            RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
            check.equal(1, 2, "task_init Exception returned on API request")
            return False

        if res.status_code != 200:
            log.error(Template("task_init api request fail, the response text is: $content").substitute(content=res.text))
            RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            check.equal(1, 2, msg="task_init api response status_code not equal 200, fail")

        try:
            res_json = res.json()
        except Exception as e:
            log.error(Template("task_init 响应内容格式化为json失败，错误信息: $e").substitute(e=e))

            RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            return

        if test_case.get('interface_var'):
            var_dict = parse_interface_var(test_case['interface_var'], res_json)
            for k, v in var_dict.items():
                init_object.interface_vars[k] = v
        log.debug(Template("task_init interface vars: $interface_var").substitute(interface_var=init_object.interface_vars))

        RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")

        if test_case.get('wait_time'):
            wait_time = float(test_case['wait_time'])
            log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
            time.sleep(wait_time)


class TestClearDatas(object):
    pass