# -*- coding: utf-8 -*-

"""
author: leo
功能: 通过脚本自动生成的待测试用例
"""
import os
import pytest
import allure
import pytz
import time
from string import Template
from datetime import datetime
from core.logs import CustomLogger
from .test_task_common import init_object
import pytest_check as check
from core.api import ApiHandler
from core.case_parse.execute_unit import VarReplace, parse_interface_var, parse_case_vars, var_add_random_str
from core.case_parse.execute_unit import datetime_translate, dyparam_parse
from core.case_parse import execute_unit as eut
from core.results import RS
from core.databases import mysql_helper


current_time = str(datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S"))
dir_with_time = current_time.split('_')[0]
file_name = os.path.basename(__file__).rstrip('.py')
log_path = os.path.join(dir_with_time, "{}_{}.log".format(file_name, current_time))
log = CustomLogger(filename=log_path).logger
class InterfaceVars(object):
    def __init__(self):
        self.interface_vars = {'clusterId': '17df109d-35b7-4a31-b8a0-815d76959b1c', 'tenant_id': 'f6d4b7a3-db29-476b-aaa2-392fad843442'}
        self.backup_vars = {}


ivs = InterfaceVars()


class TestClass(object):

    def setup_class(self):
        test_cases = [{'order': 1, 'module': '命名空间', 'casename': '新增初始化命名空间', 'description': '初始化命名空间', 'url': 'http://192.168.203.83/api/gce/namespace/create', 'method': 'POST', 'params': {'name': '{namespace_name}', 'clusterId': '{clusterId}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': {'name_space_name': '123456', 'testtest': 'test123'}, 'interface_var': '', 'wait_time': 2.0, 'hostname': 'http://192.168.203.83'}, {'order': 2, 'module': '命名空间', 'casename': '查看初始化命名空间', 'description': '查看命名空间，获取初始命名空间id', 'url': 'http://192.168.203.83/api/gce/namespace/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'detail': 'true'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': {'namespace_id': "data[?name=='{namespace_name}'].id"}, 'wait_time': '', 'hostname': 'http://192.168.203.83'}, {'order': '', 'module': 'pvc', 'casename': '新增初始化pvc', 'description': '新增初始化pvc', 'url': 'http://192.168.203.83/api/gce/pvc/create', 'method': 'POST', 'params': {'name': 'autoinitaddpvc', 'namespaceId': '{namespace_id}', 'storageClassId': 'baoliucunculei', 'storage': '10Gi', 'accessModes[0]': 'ReadWriteOnce'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': 3.0, 'hostname': 'http://192.168.203.83'}, {'order': '', 'module': 'pv', 'casename': '新增初始化pv', 'description': '新增初始化pv', 'url': 'http://192.168.203.83/api/gce/pv/create', 'method': 'POST', 'params': {'clusterId': '{clusterId}', 'name': 'autoinitaddpv', 'capacity': 10, 'pvType': 'hostPath', 'storageClassId': 'baoliucunculei', 'config': {'readOnly': 'false', 'type': 'volumesource', 'path': '/root/pvstore'}, 'accessModes[0]': 'ReadWriteOnce'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': 3.0, 'hostname': 'http://192.168.203.83'}, {'order': '', 'module': 'pv', 'casename': '查看PV列表', 'description': '查看PV列表', 'url': 'http://192.168.203.83/api/gce/pv/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'detail': 'true', 'clusterId': '{clusterId}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': {'pv_id': 'data[0].id', 'pv_name': 'data[0].name'}, 'wait_time': '', 'hostname': 'http://192.168.203.83'}, {'order': '', 'module': '无状态应用', 'casename': '创建无状态应用', 'description': '创建无状态应用', 'url': 'http://192.168.203.83/api/gce/deployment/create', 'method': 'POST', 'params': {'name': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}', 'scale': 1, 'image': 'nginx', 'environment[0].key': 'test', 'environment[0].value': 1, 'imagePullPolicy': 'IfNotPresent', 'privileged': 'false', 'allowPrivilegeEscalation': 'false'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': 3.0, 'hostname': 'http://192.168.203.83'}]
        for test_case in test_cases:
            log.info(Template("正在执行：$name用例").substitute(name=test_case['casename']))
            try:
                test_case = var_add_random_str(test_case)
                test_case = datetime_translate(test_case)
                parse_case_vars(test_case, ivs)
                test_case = VarReplace(test_case, [ivs, init_object]).var_replace()
            except Exception as e:
                log.error(Template("setup_class Exception returned on var_replace,error info: $e").substitute(e=e))

            api_info = {
                "url": test_case['url'],
                "method": test_case['method'],
                "params": test_case['params'],
                "header": test_case['header']
            }
            try:
                res = ApiHandler(api_info).api_request()
            except Exception as e:
                log.error(Template("setup_class api request fail,error info: $e").substitute(e=e))
                #  check.equal(1, 2, "setup_class Exception returned on API request")
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                continue
            if res.status_code != 200:
                log.error(Template("setup_class api request fail, the response text is: $content").substitute(content=res.text))
                #  check.equal(1, 2, msg="setup_class api response status_code not equal 200, fail")
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
                continue

            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("setup_class 响应内容格式化为json失败，错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
                continue

            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v
            log.debug(Template("setup_class interface vars: $interface_var").substitute(interface_var=ivs.interface_vars))

            RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        ivs.backup_vars = ivs.interface_vars

    def teardown_class(self):
        # ivs.interface_vars = ivs.backup_vars
        test_cases = [{'order': 1, 'module': 'pvc', 'casename': '删除pvc', 'description': '删除pvc', 'url': 'http://192.168.203.83/api/gce/pvc/delete', 'method': 'POST', 'params': {'id': 'autoinitaddpvc', 'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83'}, {'order': '', 'module': 'pv', 'casename': '删除pv', 'description': '删除pv', 'url': 'http://192.168.203.83/api/gce/pv/delete', 'method': 'POST', 'params': {'id': '{pv_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83'}, {'order': '', 'module': '命名空间', 'casename': '删除命名空间', 'description': '删除命名空间', 'url': 'http://192.168.203.83/api/gce/namespace/delete', 'method': 'POST', 'params': {'id': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83'}]
        for test_case in test_cases:
            log.info(Template("teardown_class 正在执行：$name用例").substitute(name=test_case['casename']))
            try:
                test_case = var_add_random_str(test_case)
                test_case = datetime_translate(test_case)
                parse_case_vars(test_case, ivs)
                test_case = VarReplace(test_case, [ivs, init_object]).var_replace()
            except Exception as e:
                log.error(Template("teardown_class Exception returned on var_replace,error info: $e").substitute(e=e))

            api_info = {
                "url": test_case['url'],
                "method": test_case['method'],
                "params": test_case['params'],
                "header": test_case['header']
            }

            try:
                res = ApiHandler(api_info).api_request()
            except Exception as e:
                log.error(Template("teardown_class api request fail,error info: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                # check.equal(1, 2, "teardown_class Exception returned on API request")
                continue
            if res.status_code != 200:
                log.error(Template("teardown_class api request fail, the response text is: $content").substitute(
                    content=res.text))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
                #check.equal(1, 2, "teardown_class api response status_code not equal 200, fail")
                continue

            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("teardown_class 响应内容格式化为json失败，错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
                continue

            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v
            log.debug(Template("teardown_class interface vars: $interface_var").substitute(
                interface_var=ivs.interface_vars))
            RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)


    @allure.feature("命名空间")
    @allure.story("test_查看命名空间")
    @allure.description("查看命名空间,params:{'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'detail': 'true'}")
    @pytest.mark.run(order=20001)
    def test_查看命名空间(self):
        test_case = {'order': 20001, 'module': '命名空间', 'casename': '查看命名空间', 'description': '查看命名空间', 'url': 'http://192.168.203.83/api/gce/namespace/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'detail': 'true'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': {'case_namespace_id': "data[?name=='{namespace_name}'].id"}, 'wait_time': 1.0, 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"data[0].id","data[0].name"', 'res_header': '', 'status_code': 200.0, 'db_verify': {'sql1': {'sql': 'select * from cmp.cmp_config', 'db': 'db1', 'check': {'code': 'cmp.monitorgcloud.router.host', 'value': '192.168.203.38:9090'}, 'type': '=', 'ip': '192.168.203.83', 'port': 3306, 'db_type': 'mysql', 'user': 'root', 'pwd': 'Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR'}, 'sql2': {'sql': 'select * from cmp.cmp_config', 'db': 'db1', 'check': {'name': 'monitor'}, 'type': '~', 'ip': '192.168.203.83', 'port': 3306, 'db_type': 'mysql', 'user': 'root', 'pwd': 'Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR'}}, 'expression': "len(response['data'])>1", 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("命名空间")
    @allure.story("test_新增命名空间")
    @allure.description("新增命名空间,params:{'name': '{npn}', 'clusterId': '{clusterId}'}")
    @pytest.mark.run(order=20002)
    def test_新增命名空间(self):
        test_case = {'order': 20002, 'module': '命名空间', 'casename': '新增命名空间', 'description': '新增命名空间', 'url': 'http://192.168.203.83/api/gce/namespace/create', 'method': 'POST', 'params': {'name': '{npn}', 'clusterId': '{clusterId}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': {'npn': '$autotestadd$'}, 'interface_var': '', 'wait_time': 0.9, 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': [{'url': 'http://192.168.203.83/api/gce/namespace/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'detail': 'true'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'interface_var': {'npn_id': "data[?name=='{npn}'].id"}}, {'url': 'http://192.168.203.83/api/gce/namespace/delete', 'method': 'POST', 'params': {'id': '{npn_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'wait_time': 2.0}], 'dyparam': {'sql1': {'sql': 'select * from cmp.cmp_config', 'db': 'db1', 'values': {'code_value': 'code', 'value_value': 'value'}, 'ip': '192.168.203.83', 'port': 3306, 'db_type': 'mysql', 'user': 'root', 'pwd': 'Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR'}, 'sql2': {'sql': 'select * from cmp.cmp_user', 'db': 'db1', 'values': {'user_id_mysql': 'user_id'}, 'ip': '192.168.203.83', 'port': 3306, 'db_type': 'mysql', 'user': 'root', 'pwd': 'Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR'}}, 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = [{'url': 'http://192.168.203.83/api/gce/namespace/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'detail': 'true'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'interface_var': {'npn_id': "data[?name=='{npn}'].id"}}, {'url': 'http://192.168.203.83/api/gce/namespace/delete', 'method': 'POST', 'params': {'id': '{npn_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'wait_time': 2.0}]

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("命名空间")
    @allure.story("test_查看Yaml")
    @allure.description("查看命名空间yaml文件,params:{'namespaceId': '{namespace_id}'}")
    @pytest.mark.run(order=20006)
    def test_查看Yaml(self):
        test_case = {'order': 20006, 'module': '命名空间', 'casename': '查看Yaml', 'description': '查看命名空间yaml文件', 'url': 'http://192.168.203.83/api/gce/namespace/yaml', 'method': 'POST', 'params': {'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': 1.0, 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"apiVersion","items","kind"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': {'sql1': {'sql': 'select * from cmp.cmp_config', 'db': 'db1', 'values': {'code_value': 'code', 'value_value': 'value'}, 'ip': '192.168.203.83', 'port': 3306, 'db_type': 'mysql', 'user': 'root', 'pwd': 'Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR'}}, 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pvc")
    @allure.story("test_创建pvc")
    @allure.description("创建pvc,params:{'name': 'autoaddpvc', 'namespaceId': '{namespace_id}', 'storageClassId': 'baoliucunculei', 'storage': '10Gi', 'accessModes[0]': 'ReadWriteOnce'}")
    @pytest.mark.run(order=20007)
    def test_创建pvc(self):
        test_case = {'order': 20007, 'module': 'pvc', 'casename': '创建pvc', 'description': '创建pvc', 'url': 'http://192.168.203.83/api/gce/pvc/create', 'method': 'POST', 'params': {'name': 'autoaddpvc', 'namespaceId': '{namespace_id}', 'storageClassId': 'baoliucunculei', 'storage': '10Gi', 'accessModes[0]': 'ReadWriteOnce'}, 'header': {'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': {'now': '<#dnow()>', 'now5': '<#d2020-10-10 00:00:00+10>'}, 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': {'requestId': '<#reg>\\w+-\\w+-\\w+-\\w+-\\w+'}, 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pvc")
    @allure.story("test_查看PVC列表")
    @allure.description("查看PVC列表信息,params:{'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}'}")
    @pytest.mark.run(order=20008)
    def test_查看PVC列表(self):
        test_case = {'order': 20008, 'module': 'pvc', 'casename': '查看PVC列表', 'description': '查看PVC列表信息', 'url': 'http://192.168.203.83/api/gce/pvc/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': {'now2': '<#dnow()+10>'}, 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"data"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pvc")
    @allure.story("test_查看PVC基本信息")
    @allure.description("查看PVC基本信息,params:{'id': 'autoinitaddpvc', 'namespaceId': '{namespace_id}'}")
    @pytest.mark.run(order=20009)
    def test_查看PVC基本信息(self):
        test_case = {'order': 20009, 'module': 'pvc', 'casename': '查看PVC基本信息', 'description': '查看PVC基本信息', 'url': 'http://192.168.203.83/api/gce/pvc/detail', 'method': 'POST', 'params': {'id': 'autoinitaddpvc', 'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': {'now3': '<#d2021-02-02 10:01:01+10>'}, 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': {'pvc.name': 'autoinitaddpvc'}, 'res_text': '', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pvc")
    @allure.story("test_查看PVC事件")
    @allure.description("查看PVC事件,params:{'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'namespaceId': '{namespace_id}', 'name': 'autoinitaddpvc', 'kind': 'PersistentVolumeClaim'}")
    @pytest.mark.run(order=20005)
    def test_查看PVC事件(self):
        test_case = {'order': 20005, 'module': 'pvc', 'casename': '查看PVC事件', 'description': '查看PVC事件', 'url': 'http://192.168.203.83/api/gce/event/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'clusterId': '{clusterId}', 'namespaceId': '{namespace_id}', 'name': 'autoinitaddpvc', 'kind': 'PersistentVolumeClaim'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': {'now4': '<#d2021-02-02 10:01:01>'}, 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"data","requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pv")
    @allure.story("test_新增pv")
    @allure.description("新增pv,params:{'clusterId': '{clusterId}', 'name': 'autoaddpv', 'capacity': 10, 'pvType': 'hostPath', 'storageClassId': 'baoliucunculei', 'config': {'readOnly': 'false', 'type': 'volumesource', 'path': '/root/pvstore'}, 'accessModes[0]': 'ReadWriteOnce'}")
    @pytest.mark.run(order=20010)
    def test_新增pv(self):
        test_case = {'order': 20010, 'module': 'pv', 'casename': '新增pv', 'description': '新增pv', 'url': 'http://192.168.203.83/api/gce/pv/create', 'method': 'POST', 'params': {'clusterId': '{clusterId}', 'name': 'autoaddpv', 'capacity': 10, 'pvType': 'hostPath', 'storageClassId': 'baoliucunculei', 'config': {'readOnly': 'false', 'type': 'volumesource', 'path': '/root/pvstore'}, 'accessModes[0]': 'ReadWriteOnce'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"pagination"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pv")
    @allure.story("test_查看PV列表")
    @allure.description("查看PV列表,params:{'pageNumber': 1, 'limit': 10, 'detail': 'true', 'clusterId': '{clusterId}'}")
    @pytest.mark.run(order=20011)
    def test_查看PV列表(self):
        test_case = {'order': 20011, 'module': 'pv', 'casename': '查看PV列表', 'description': '查看PV列表', 'url': 'http://192.168.203.83/api/gce/pv/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'detail': 'true', 'clusterId': '{clusterId}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"pagination"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pv")
    @allure.story("test_查看PV基本信息")
    @allure.description("查看PV基本信息,params:{'clusterId': '{clusterId}', 'id': '{pv_id}'}")
    @pytest.mark.run(order=20012)
    def test_查看PV基本信息(self):
        test_case = {'order': 20012, 'module': 'pv', 'casename': '查看PV基本信息', 'description': '查看PV基本信息', 'url': 'http://192.168.203.83/api/gce/pv/detail', 'method': 'POST', 'params': {'clusterId': '{clusterId}', 'id': '{pv_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"pv.id"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pv")
    @allure.story("test_查看PV事件")
    @allure.description("查看PV事件,params:{'pageNumber': 1, 'limit': 10, 'id': '{pv_id}'}")
    @pytest.mark.run(order=20003)
    def test_查看PV事件(self):
        test_case = {'order': 20003, 'module': 'pv', 'casename': '查看PV事件', 'description': '查看PV事件', 'url': 'http://192.168.203.83/api/gce/event/pv_page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'id': '{pv_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"pagination","data"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("pv")
    @allure.story("test_编辑PV")
    @allure.description("编辑PV,params:{'name': '{pv_name}', 'capacity': 11, 'pvType': 'hostPath', 'clusterId': '{clusterId}', 'storageClassId': 'baoliucunculei', 'config': {'readOnly': 'false', 'type': 'hostpathvolumesource', 'path': '/root/pvstore'}, 'accessModes[0]': 'ReadWriteOnce', 'id': '{pv_id}'}")
    @pytest.mark.run(order=20013)
    def test_编辑PV(self):
        test_case = {'order': 20013, 'module': 'pv', 'casename': '编辑PV', 'description': '编辑PV', 'url': 'http://192.168.203.83/api/gce/pv/update', 'method': 'POST', 'params': {'name': '{pv_name}', 'capacity': 11, 'pvType': 'hostPath', 'clusterId': '{clusterId}', 'storageClassId': 'baoliucunculei', 'config': {'readOnly': 'false', 'type': 'hostpathvolumesource', 'path': '/root/pvstore'}, 'accessModes[0]': 'ReadWriteOnce', 'id': '{pv_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("无状态应用")
    @allure.story("test_查看无状态应用列表")
    @allure.description("查看无状态应用列表,params:{'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}")
    @pytest.mark.run(order=20014)
    def test_查看无状态应用列表(self):
        test_case = {'order': 20014, 'module': '无状态应用', 'casename': '查看无状态应用列表', 'description': '查看无状态应用列表', 'url': 'http://192.168.203.83/api/gce/deployment/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"data"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("无状态应用")
    @allure.story("test_编辑无状态应用")
    @allure.description("编辑无状态应用,params:{'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}', 'data': {'name': 'aaa', 'namespaceId': '{namespace_id}', 'scale': 2, 'image': 'nginx', 'environment': [], 'ports': [], 'imagePullPolicy': 'IfNotPresent', 'privileged': 'false', 'allowPrivilegeEscalation': 'false'}}")
    @pytest.mark.run(order=20015)
    def test_编辑无状态应用(self):
        test_case = {'order': 20015, 'module': '无状态应用', 'casename': '编辑无状态应用', 'description': '编辑无状态应用', 'url': 'http://192.168.203.83/api/gce/deployment/edit', 'method': 'POST', 'params': {'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}', 'data': {'name': 'aaa', 'namespaceId': '{namespace_id}', 'scale': 2, 'image': 'nginx', 'environment': [], 'ports': [], 'imagePullPolicy': 'IfNotPresent', 'privileged': 'false', 'allowPrivilegeEscalation': 'false'}}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("无状态应用")
    @allure.story("test_查看无状态应用yaml")
    @allure.description("查看无状态应用yaml,params:{'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}'}")
    @pytest.mark.run(order=20016)
    def test_查看无状态应用yaml(self):
        test_case = {'order': 20016, 'module': '无状态应用', 'casename': '查看无状态应用yaml', 'description': '查看无状态应用yaml', 'url': 'http://192.168.203.83/api/gce/deployment/yaml', 'method': 'POST', 'params': {'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': {'metadata.name': 'autoinitaddwztyy'}, 'res_text': '"apiVersion","kind","spec","status"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("无状态应用")
    @allure.story("test_停止无状态应用编排")
    @allure.description("停止无状态应用编排,params:{'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}'}")
    @pytest.mark.run(order=20017)
    def test_停止无状态应用编排(self):
        test_case = {'order': 20017, 'module': '无状态应用', 'casename': '停止无状态应用编排', 'description': '停止无状态应用编排', 'url': 'http://192.168.203.83/api/gce/deployment/pause', 'method': 'POST', 'params': {'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("无状态应用")
    @allure.story("test_恢复无状态应用编排")
    @allure.description("恢复无状态应用编排,params:{'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}'}")
    @pytest.mark.run(order=20018)
    def test_恢复无状态应用编排(self):
        test_case = {'order': 20018, 'module': '无状态应用', 'casename': '恢复无状态应用编排', 'description': '恢复无状态应用编排', 'url': 'http://192.168.203.83/api/gce/deployment/resume', 'method': 'POST', 'params': {'id': 'autoinitaddwztyy', 'namespaceId': '{namespace_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("容器组")
    @allure.story("test_查看容器组列表")
    @allure.description("查看容器组列表,params:{'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}")
    @pytest.mark.run(order=20019)
    def test_查看容器组列表(self):
        test_case = {'order': 20019, 'module': '容器组', 'casename': '查看容器组列表', 'description': '查看容器组列表', 'url': 'http://192.168.203.83/api/gce/pod/page', 'method': 'POST', 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"pagination"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': '', 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = []
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("容器组")
    @allure.story("test_查看容器组细节")
    @allure.description("查看容器组细节,params:{'clusterId': '{clusterId}', 'namespaceId': '{namespace_id}', 'id': '{docker_id}'}")
    @pytest.mark.run(order=20020)
    def test_查看容器组细节(self):
        test_case = {'order': 20020, 'module': '容器组', 'casename': '查看容器组细节', 'description': '查看容器组细节', 'url': 'http://192.168.203.83/api/gce/pod/detail', 'method': 'POST', 'params': {'clusterId': '{clusterId}', 'namespaceId': '{namespace_id}', 'id': '{docker_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': {'pod.name': '{docker_id}'}, 'res_text': '', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': [{'url': 'http://192.168.203.83/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}, 'wait_time': 2.0}], 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = [{'url': 'http://192.168.203.83/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}, 'wait_time': 2.0}]
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("容器组")
    @allure.story("test_查看容器组监控数据")
    @allure.description("查看容器组监控数据,params:{'resourceId': '{docker_id}', 'meters[0]': 'container.net_rx_rate', 'meters[1]': 'container.fs_reads_rate', 'resourceType': 'container'}")
    @pytest.mark.run(order=20021)
    def test_查看容器组监控数据(self):
        test_case = {'order': 20021, 'module': '容器组', 'casename': '查看容器组监控数据', 'description': '查看容器组监控数据', 'url': 'http://192.168.203.83/api/mesh/monitor/monitor/DetailResource', 'method': 'POST', 'params': {'resourceId': '{docker_id}', 'meters[0]': 'container.net_rx_rate', 'meters[1]': 'container.fs_reads_rate', 'resourceType': 'container'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': {'data.list.resourceName': '{docker_id}'}, 'res_text': '', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': [{'url': 'http://192.168.203.38/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}}], 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = [{'url': 'http://192.168.203.38/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}}]
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("容器组")
    @allure.story("test_查看容器组的yaml")
    @allure.description("查看容器组的yaml,params:{'namespaceId': '{namespace_id}', 'id': '{docker_id}'}")
    @pytest.mark.run(order=20022)
    def test_查看容器组的yaml(self):
        test_case = {'order': 20022, 'module': '容器组', 'casename': '查看容器组的yaml', 'description': '查看容器组的yaml', 'url': 'http://192.168.203.83/api/gce/pod/yaml', 'method': 'POST', 'params': {'namespaceId': '{namespace_id}', 'id': '{docker_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': {'metadata.name': '{docker_id}'}, 'res_text': '', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': [{'url': 'http://192.168.203.38/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}}], 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = [{'url': 'http://192.168.203.38/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}}]
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)


    @allure.feature("容器组")
    @allure.story("test_删除容器组")
    @allure.description("删除容器组,params:{'namespaceId': '{namespace_id}', 'id': '{docker_id}'}")
    @pytest.mark.run(order=20023)
    def test_删除容器组(self):
        test_case = {'order': 20023, 'module': '容器组', 'casename': '删除容器组', 'description': '删除容器组', 'url': 'http://192.168.203.83/api/gce/pod/delete', 'method': 'POST', 'params': {'namespaceId': '{namespace_id}', 'id': '{docker_id}'}, 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'case_vars': '', 'interface_var': '', 'wait_time': '', 'hostname': 'http://192.168.203.83', 'verify_fields': '', 'res_text': '"requestId"', 'res_header': '', 'status_code': 200.0, 'db_verify': '', 'expression': '', 'res_time': 2.0, 'init': [{'url': 'http://192.168.203.38/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}}], 'restore': '', 'dyparam': '', 'header_manager': '', 'iteration': 1.0}
        # ivs.interface_vars = ivs.backup_vars
        log.info("="*60)
        log.info(Template("正在执行：$name").substitute(name=test_case['casename']))

        init_cases = [{'url': 'http://192.168.203.38/api/gce/pod/page', 'method': 'POST', 'header': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Auth-Token': '{token}', 'x-gce-tenant-id': '{tenant_id}'}, 'params': {'pageNumber': 1, 'limit': 10, 'namespaceId': '{namespace_id}', 'clusterId': '{clusterId}'}, 'interface_var': {'docker_id': 'data[0].name'}}]
        restore_cases = []

        # 执行测试用例中的初始化步骤
        if init_cases:
            for init_case in init_cases:
                log.info(Template("执行用例中的初始化接口：$name").substitute(name=init_case['url']))
                init_case = VarReplace(init_case, [ivs, init_object]).var_replace()
                self.exec_init_case(init_case)

        test_case = var_add_random_str(test_case)
        test_case = datetime_translate(test_case)
        parse_case_vars(test_case, ivs)
        dyparam_parse(test_case, ivs)
        test_case = VarReplace(test_case, [ivs, init_object]).var_replace()

        api_info = {
            "url": test_case['url'],
            "method": test_case['method'],
            "params": test_case['params'],
            "header": test_case['header']
        }

        try:
            iteration = int(test_case['iteration'])
        except Exception as e:
            log.error(Template("iteration to integer failed,set iteration to 1,error info: $e").substitute(e=e))
            iteration = 1
        for index in range(0, iteration):
            flag = True
            log.info(Template("execute $index times request").substitute(index=index + 1))
            res = ApiHandler(api_info).api_request()
            try:
                res_json = res.json()
            except Exception as e:
                log.error(Template("api请求响应转换为json失败,错误信息: $e").substitute(e=e))
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'],
                        test_case['params'], test_case['header'], "request error"], "fail")
                check.equal(1, 2, msg=Template("api请求响应转换为json失败,接口返回内容：$res,错误信息：$e").substitute(res=res.text, e=e))
                continue

            if test_case.get("verify_fields"):
                msg = eut.check_verify_fields(test_case["verify_fields"], res_json)
                if msg:
                    log.error(Template("字段校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("字段校验成功").substitute())

            if test_case.get("res_text"):
                msg = eut.check_response_text(test_case['res_text'], res_json)
                if msg:
                    log.error(Template("响应内容校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应内容校验成功").substitute())

            if test_case.get("res_header"):
                msg = eut.check_response_header(test_case['res_header'], res.headers)
                if msg:
                    log.error(Template("响应头校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应头校验成功").substitute())

            if test_case.get("status_code"):
                msg = eut.check_status_code(test_case['status_code'], res.status_code)
                if msg:
                    log.error(Template("响应状态码校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应状态码校验成功").substitute())

            if test_case.get("res_time"):
                msg = eut.check_response_time(test_case['res_time'], res.elapsed.total_seconds())
                if msg:
                    log.error(Template("响应时间校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("响应时间校验成功").substitute())

            if test_case.get("expression"):
                msg = eut.check_pyexpression(test_case['expression'], res_json)
                if msg:
                    log.error(Template("py表达式校验失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("py表达式校验成功").substitute())
            if test_case.get("db_verify"):
                msg = eut.check_db_verify(test_case['db_verify'])
                if msg:
                    log.error(Template("数据库验证失败，失败信息：$msg").substitute(msg=msg))
                    flag = False
                    check.equal(1, 2, msg=msg)
                else:
                    log.info(Template("数据库验证成功").substitute())

            if flag:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "pass")
            else:
                RS.append_row(file_name, [test_case['casename'], test_case['url'], test_case['method'], test_case['params'],
                                      test_case['header'], res.text, res.status_code, res.elapsed.total_seconds()],
                          "fail")
            if test_case.get('interface_var'):
                var_dict = parse_interface_var(test_case['interface_var'], res_json)
                for k, v in var_dict.items():
                    ivs.interface_vars[k] = v

            if test_case.get('wait_time'):
                wait_time = float(test_case['wait_time'])
                log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
                time.sleep(wait_time)

        # 执行测试用例中的数据恢复步骤
        if restore_cases:
            for restore_case in restore_cases:
                restore_case = VarReplace(restore_case, [ivs, init_object]).var_replace()
                self.exec_restore_case(restore_case)

    def exec_init_case(self, case):
        log.info("**********执行初始化用例**********")
        try:
            case = var_add_random_str(case)
            case = datetime_translate(case)
            parse_case_vars(case, ivs)
            dyparam_parse(case, ivs)
            case = VarReplace(case, [self, ivs, init_object]).var_replace()
        except Exception as e:
            log.error(Template("exec_restore_case Exception returned on var_replace,error info: $$e").substitute(e=e))

        init_api_info = {
            "url": case["url"],
            "method": case["method"],
            "params": case["params"],
            "header": case["header"]
        }

        try:
            res = ApiHandler(init_api_info).api_request()
        except Exception as e:
            log.error(Template("exec_init_case api request fail,error info: $$e").substitute(e=e))
            # check.equal(1, 2, "exec_init_case Exception returned on API request")
            return False

        if res.status_code != 200:
            log.error(Template("exec_init_case api request fail, the response text is: $$content").substitute(
                content=res.text))
            log.error(Template("exec_init_case api response is: $$res").substitute(res=res.json()))
            # check.equal(1, 2, "exec_init_case api response status_code not equal 200, fail")
            return False

        try:
            res_json = res.json()
        except Exception as e:
            log.error(Template("exec_init_case 响应内容格式化为json失败，错误信息: $$e").substitute(e=e))
            return False

        if case.get("interface_var"):
            var_dict = parse_interface_var(case['interface_var'], res_json)
            for k, v in var_dict.items():
                ivs.interface_vars[k] = v

        if case.get('wait_time'):
            wait_time = float(case['wait_time'])
            log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
            time.sleep(wait_time)
        log.info("**********初始化用例执行完毕**********")

    def exec_restore_case(self, case):
        log.info("**********执行恢复用例**********")
        try:
            case = var_add_random_str(case)
            case = datetime_translate(case)
            parse_case_vars(case, ivs)
            dyparam_parse(case, ivs)
            case = VarReplace(case, [self, ivs, init_object]).var_replace()
        except Exception as e:
            log.error(Template("exec_restore_case Exception returned on var_replace,error info: $$e").substitute(e=e))
        restore_api_info = {
            "url": case["url"],
            "method": case["method"],
            "params": case["params"],
            "header": case["header"]
        }

        try:
            res = ApiHandler(restore_api_info).api_request()
        except Exception as e:
            log.error(Template("exec_restore_case api request fail,error info: $$e").substitute(e=e))
            # check.equal(1, 2, "exec_restore_case Exception returned on API request")
            return False

        if res.status_code != 200:
            log.error(Template("exec_restore_case api request fail, the response text is: $$content").substitute(
                content=res.text))
            log.error(Template("exec_restore_case api response is: $$res").substitute(res=res.json()))
            # check.equal(1, 2, "exec_restore_case api response status_code not equal 200, fail")
            return False

        try:
            res_json = res.json()
        except Exception as e:
            log.error(Template("exec_restore_case 响应内容格式化为json失败，错误信息: $$e").substitute(e=e))
            return False

        if case.get("interface_var"):
            var_dict = parse_interface_var(case['interface_var'], res_json)
            for k, v in var_dict.items():
                ivs.interface_vars[k] = v

        if case.get('wait_time'):
            wait_time = float(case['wait_time'])
            log.info("用例设置了等待时间，等待{}秒,请等待。。。".format(str(wait_time)))
            time.sleep(wait_time)
        log.info("**********恢复用例执行完毕**********")

    def _set_interface_var(self, var):

        for k, v in var.items():
            ivs.interface_vars[k] = v


