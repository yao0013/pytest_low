# -*- coding: utf-8 -*-
"""
author: lufoqin
func: 把待测试的Excel表格中的用例，转换为json格式存储
"""
import os
import string
import sys
import xlrd
import ast
from core.logs import log
from core.case_parse.execute_unit import var_add_random_str
from core.CustomExceptions import JsonSerializeException
from configs import settings


class Process(object):
    base_configs = None  # 基础配置sheet
    global_vars = None  # 全局变量sheet

    def __init__(self, filepath):
        if not os.path.isfile(filepath):
            log.error(string.Template("test case file not found, please check! $filepath").substitute(filepath=filepath))
            raise FileNotFoundError("test case file not found, please check!")
        self.filepath = filepath
        self.excel_fields = settings.excel_fields
        self.init_case = None  # 数据初始化sheet
        self.restore_case = None  # 数据恢复sheet
        self.base_configs = None  # 基础配置sheet
        self.all_sheets = None  # Excel文件所有sheet
        self.testsuites = {}  # 除了已有固定的sheet外的其他测试sheet
        self.testsuite_local_vars_line_name="local_line"
        self.testsuite_init_line_name = "init_line"
        self.testsuites_restore_line_name = "restore_line"
        self.testsuites_testcase_line_name = "testcase_line"
        self._read_file()
        self.parse_base_configs()
        self.parse_global_vars()
        self.parse_init_datas()
        self.parse_testsuite()
        self.parse_restore_datas()
        self.cases_order()

    def _read_file(self):
        """
        读取Excel文件，解析基础配置sheet，数据初始化sheet， 数据恢复sheet， 公共方法sheet和所有测试套sheet
        :return:
        """
        all_sheets = {}
        test_suite = []
        try:
            workbook = xlrd.open_workbook(self.filepath)

        except Exception as e:
            log.exception(string.Template("open testcase file fail, please check! %e").substitute(e=e))
            return False

        sheet_names = workbook.sheet_names()
        log.debug(string.Template("testcase sheets: $sheet_names").substitute(sheet_names=sheet_names))
        # print(sheet_names)

        if '基础配置' in sheet_names:
            base_configs = workbook.sheet_by_name('基础配置')
            all_sheets['base_configs'] = base_configs
            sheet_names.remove('基础配置')
        if '数据初始化' in sheet_names:
            initialize_datas = workbook.sheet_by_name('数据初始化')
            all_sheets['initialize_datas'] = initialize_datas
            sheet_names.remove('数据初始化')
        if '数据恢复' in sheet_names:
            restore = workbook.sheet_by_name('数据恢复')
            all_sheets['restore'] = restore
            sheet_names.remove('数据恢复')
        if '公共方法' in sheet_names:
            common_func = workbook.sheet_by_name('公共方法')
            all_sheets['common_func'] = common_func
            sheet_names.remove('公共方法')
        if '全局变量' in sheet_names:
            global_vars = workbook.sheet_by_name('全局变量')
            all_sheets['global_vars'] = global_vars
            sheet_names.remove('全局变量')
        for sheet in sheet_names:
            test_suite.append(workbook.sheet_by_name(sheet))
        log.info(string.Template("All the test suite that need to be tested: $test_suite").substitute(test_suite=test_suite))
        all_sheets['testsuites'] = test_suite
        self.all_sheets = all_sheets
        return all_sheets

    @classmethod
    def _read_sheet_rows(cls, sheet):
        """
        获取整个sheet表的所有行数据
        :param sheet:
        :return: 所有行的数据
        """
        try:
            return sheet.get_rows()
        except Exception as e:
            log.error(string.Template("get sheet rows fail, sheet is: $sheet").substitute(sheet=sheet.name))
            log.exception(e)

    def _read_case_content(self, row, sheet_type):
        """
        读取row的字段值
        :param row: 每行的字段
        :param sheet_type: 区分是否是测试套sheet，值 == testsuite时，读取需校验的字段
        :return: 序列化后的行字段
        """
        mapper = self.excel_fields
        case_info = {}
        case_info['order'] = row[mapper['order']].value
        case_info['module'] = row[mapper['module']].value
        case_info['casename'] = row[mapper['casename']].value
        case_info['description'] = row[mapper['description']].value
        case_info['url'] = row[mapper['url']].value.strip()
        case_info['method'] = row[mapper['method']].value.strip()
        case_info['params'] = row[mapper['params']].value
        case_info['header'] = row[mapper['header']].value
        case_info['case_vars'] = row[mapper['case_vars']].value
        case_info['interface_var'] = row[mapper['interface_var']].value
        case_info["wait_time"] = row[mapper['wait_time']].value
        case_info['hostname'] = self.base_configs.get('hostname') if self.base_configs.get('hostname') else ""
        if sheet_type == 'testcase':
            case_info['verify_fields'] = row[mapper['verify_fields']].value
            case_info['res_text'] = row[mapper['res_text']].value
            case_info['res_header'] = row[mapper['res_header']].value
            case_info['status_code'] = row[mapper['status_code']].value
            case_info['db_verify'] = row[mapper['db_verify']].value
            case_info['expression'] = row[mapper['expression']].value
            case_info['res_time'] = row[mapper['res_time']].value
            case_info['init'] = row[mapper['init']].value
            case_info['restore'] = row[mapper['restore']].value
            case_info['dyparam'] = row[mapper['dyparam']].value
            case_info['header_manager'] = row[mapper['header_manager']].value
            case_info['iteration'] = row[mapper['iteration']].value

        return case_info

    def _read_localvars_content(self,row):
        """
        读取局部变量信息
        """
        mapper = self.excel_fields
        localvar_info = {}
        localvar_info[row[mapper['local_var_key']].value]=row[mapper['local_var_value']].value

        return localvar_info


    def parse_base_configs(self):
        """
        获取基础配置信息，将基础配置信息加入Process类属性
        :return:
        """
        base_configs_dict = {}
        sheet = self.all_sheets.get('base_configs')
        if not sheet:
            log.info('testcase文件没有"基础配置"sheet')
            self.base_configs = base_configs_dict
            Process.base_configs = base_configs_dict
            return None
        rows = self._read_sheet_rows(sheet)

        for row in list(rows)[1:]:
            key_content = row[0].value
            value_content = row[1].value
            if key_content:

                if key_content == 'hostname':
                    Process.hostname = row[1].value
                    base_configs_dict['hostname'] = value_content if (value_content).startswith('http://') else "http://" + value_content
                elif key_content == 'start_time':
                    Process.start_time = value_content
                    base_configs_dict['start_time'] = value_content
                elif key_content == 'database':
                    database = value_content
                    if database:
                        res = Serialize.database_config_check(database)
                        if not res:
                            log.error('数据库配置内容有异常，请检查')
                            sys.exit(-1)
                        Process.database = res
                        base_configs_dict['database'] = res
                elif key_content == 'mail_switch' or key_content == 'email_switch':
                    mail_switch = value_content or "true"
                    if mail_switch.lower() == 'true':
                        mail_switch = True
                    else:
                        mail_switch = False
                    log.info('mail notify switch is: {}'.format(mail_switch))
                    base_configs_dict['mail_switch'] = mail_switch
                elif key_content == 'dingrobot_switch':
                    dingrobot_switch = value_content or "true"
                    if dingrobot_switch.lower() == "true":
                        dingrobot_switch = True
                    else:
                        dingrobot_switch = False
                    log.info('dingrobot notify switch is {}'.format(dingrobot_switch))
                    base_configs_dict['dingrobot_switch'] = dingrobot_switch
                elif key_content == 'mail_receivers' or key_content == "email_receivers":
                    mail_receiver = value_content or ""
                    mail_receiver = mail_receiver.split(',')
                    log.info('mail receivers is: {}'.format(mail_receiver))
                    base_configs_dict['mail_receivers'] = mail_receiver

                else:
                    log.warning(string.Template("base configs not supports this fields: $fields").substitute(fields=value_content))
        self.base_configs = base_configs_dict
        Process.base_configs = base_configs_dict

    @classmethod
    def _case_format(cls, case):
        """
        对表格数据进行格式化校验和进行序列化
        :return: 序列化后的用例
        """
        try:
            return Serialize(case).serialize()
        except JsonSerializeException:
            log.error(string.Template("Excel文件数据有误，请检查，错误用例：$case").substitute(case=case))
            sys.exit(-1)

    def parse_init_datas(self):
        """
        解析初始化sheet
        1. 序列化testcase，以字典格式存放
        :return:
        """
        init_cases = []
        init_cases_serialize = []
        sheet = self.all_sheets.get('initialize_datas')
        if not sheet:
            log.info('testcase文件没有"数据初始化"sheet')
            self.init_case = []
            return None
        rows = self._read_sheet_rows(sheet)

        rows = list(rows)
        for row in rows[2:]:
            if self.is_valid_case(row):
                init_cases.append(self._read_case_content(row, sheet_type="init"))
        log.info(string.Template("initialize test case info: $init_case").substitute(init_case=init_cases))

        for case in init_cases:
            init_cases_serialize.append(self._case_format(case))

        self.init_case = init_cases_serialize

    def parse_restore_datas(self):
        """
        解析restore sheet
        1. 序列化testcase，以字典格式存放
        :return:
        """
        restore_cases = []
        restore_case_serialize = []
        sheet = self.all_sheets.get('restore')
        if not sheet:
            log.info('testcase文件没有"数据恢复"sheet')
            self.restore_case = []
            return None
        rows = self._read_sheet_rows(sheet)

        rows = list(rows)
        for row in rows[2:]:
            if self.is_valid_case(row):
                restore_cases.append(self._read_case_content(row, sheet_type="restore"))
        log.info(string.Template("restore test case info: $restore_case").substitute(restore_case=restore_cases))
        for case in restore_cases:
            restore_case_serialize.append(self._case_format(case))
        self.restore_case = restore_case_serialize

    def parse_testsuite(self):
        """
        func: 解析测试套用例，并存入对象testsuites属性中
        :return:
        """
        testsuites = {}
        sheets = self.all_sheets['testsuites']
        if not sheets:
            log.warn('testcase文件没有需要测试的sheet，请检查')
            return None
        for sheet in sheets:
            sheet_name = sheet.name
            testsuites[sheet_name] = {}
            rows = list(sheet.get_rows())
            case_line_info = self.parse_testsuite_fields_lines(rows)
            for case_type, lines in case_line_info.items():
                if case_type == self.testsuite_init_line_name:
                    testsuites[sheet_name]['init_case'] = []
                    for row in rows[lines[0]:lines[1]]:
                        if self.is_valid_case(row):
                            testsuites[sheet_name]['init_case'].append(self._read_case_content(row, sheet_type="init"))
                elif case_type == self.testsuites_restore_line_name:
                    testsuites[sheet_name]['restore_case'] = []
                    for row in rows[lines[0]+2:lines[1]]:
                        if self.is_valid_case(row):
                            testsuites[sheet_name]['restore_case'].append(self._read_case_content(row, sheet_type="restore"))
                elif case_type == self.testsuites_testcase_line_name:
                    testsuites[sheet_name]["testcase"] = []
                    for row in rows[lines[0]+2:lines[1]]:
                        if self.is_valid_case(row):
                            testsuites[sheet_name]["testcase"].append(self._read_case_content(row, sheet_type="testcase"))
                elif case_type==self.testsuite_local_vars_line_name:
                    testsuites[sheet_name]['local_vars']=[]
                    for row in rows[lines[0]+2:lines[1]]:
                        if row[1].value !='':
                            testsuites[sheet_name]["local_vars"].append(self._read_localvars_content(row))
            # print(testsuites[sheet_name])
            self.testsuites[sheet_name] = self.serialize_testsuite(testsuites[sheet_name])

    def parse_global_vars(self):
        """
        解析全局变量 sheet
        1. 解析变量名和变量值，以字典格式存入对象中
        :return:
        """
        global_vars = {}
        mapper = self.excel_fields
        sheet = self.all_sheets.get('global_vars')
        if not sheet:
            log.info('testcase文件没有"全局变量"sheet')
            return None
        rows = self._read_sheet_rows(sheet)

        rows = list(rows)
        for row in rows[1:]:
            global_vars[row[mapper['global_var_key']].value] = row[mapper['global_var_value']].value
        log.info(string.Template("global_vars info: $global_vars").substitute(global_vars=global_vars))
        global_vars = var_add_random_str(global_vars)
        Process.global_vars = global_vars

    def serialize_testsuite(self, testsuite):
        """
        func: 将所有测试用例转化为json格式
        :param testsuite:
        :return:
        """
        testsuite_serialize = {}

        for data_type, data in testsuite.items():
            case_serialize = []
            localvar_serialize={}
            if data_type !='local_vars':
                for case in data:
                    case_serialize.append(self._case_format(case))
                testsuite_serialize[data_type] = case_serialize
            elif data_type =='local_vars':
                for localvar in data:
                    for keystr in localvar:
                        localvar_serialize[keystr]=localvar[keystr]
                testsuite_serialize[data_type]=localvar_serialize
        return testsuite_serialize

    def parse_testsuite_fields_lines(self, content):
        """
        func: 解析测试sheet中局部变量、初始化数据、接口测试、数据恢复所在的行位置
        :param content: sheet所有行的数据
        :return: 局部变量、初始化数据、接口测试、数据恢复所在的行位置
        """
        lines_info = {}
        lines_info_result = {}
        if not isinstance(content, list):
            raise TypeError("params is not a list object")
        print(content)
        for num in range(0, len(content)):
            if '局部变量' ==content[num][0].value:
                lines_info[self.testsuite_local_vars_line_name]=num
            if '初始化数据' == content[num][0].value:
                lines_info[self.testsuite_init_line_name] = num
            elif '接口测试' == content[num][0].value:
                lines_info[self.testsuites_testcase_line_name] = num
            elif '数据恢复' == content[num][0].value:
                lines_info[self.testsuites_restore_line_name] = num
        log.info(string.Template("line info: $lines_info").substitute(lines_info=lines_info))
        lines_info_order = sorted(lines_info.items(), key=lambda x: x[1], reverse=False)
        fields_num = len(lines_info_order)
        if fields_num==4:
            lines_info_result[lines_info_order[0][0]] = (lines_info_order[0][1], lines_info_order[1][1])
            lines_info_result[lines_info_order[1][0]] = (lines_info_order[1][1], lines_info_order[2][1])
            lines_info_result[lines_info_order[2][0]] = (lines_info_order[2][1], lines_info_order[3][1])
            lines_info_result[lines_info_order[3][0]] = (lines_info_order[3][1], len(content))
        if fields_num == 3:
            lines_info_result[lines_info_order[0][0]] = (lines_info_order[0][1], lines_info_order[1][1])
            lines_info_result[lines_info_order[1][0]] = (lines_info_order[1][1], lines_info_order[2][1])
            lines_info_result[lines_info_order[2][0]] = (lines_info_order[2][1], len(content))
        elif fields_num == 2:
            lines_info_result[lines_info_order[0][0]] = (lines_info_order[0][1], lines_info_order[1][1])
            lines_info_result[lines_info_order[1][0]] = (lines_info_order[1][1], len(content))
        elif fields_num == 1:
            lines_info_result[lines_info_order[0][0]] = (lines_info_order[0][1], len(content))
        log.debug(string.Template("lines_info_result: $lines_info_result").substitute(lines_info_result=lines_info_result))
        return lines_info_result

    def is_valid_case(self, case):
        mapper = self.excel_fields
        if case[mapper['url']].value and case[mapper['url']].value.strip() != 'url':
            return True
        else:
            return False

    def cases_order(self):
        """
        对用例根据用例执行顺序进行编排
        优先级：
            1. 初始化测试套的用例>测试套用例>恢复数据测试套的用例
            2. 有用例编号的执行顺序>无编号的执行顺序
        :return:
        """
        init_case = self.init_case
        restore_case = self.restore_case
        testsuites = self.testsuites
        base_num = 10000
        testsuite_num = len(testsuites)+2
        max_base_num = base_num * testsuite_num
        self.init_case = self._order_for_testcase(init_case, base_num)
        self.restore_case = self._order_for_testcase(restore_case, max_base_num)
        index = 2
        for sheet_name, testcases in testsuites.items():
            if testcases:
                case_base_num = base_num * index
                if testcases.get('init_case'):
                    testcases['init_case'] = self._order_for_list_case(testcases['init_case'])
                if testcases.get('restore_case'):
                    testcases['restore_case'] = self._order_for_list_case(testcases['restore_case'])
                if testcases.get('testcase'):
                    testcases['testcase'] = self._order_for_testcase(testcases['testcase'], case_base_num)
                self.testsuites[sheet_name] = testcases
                index += 1

    def _order_for_list_case(self, cases):
        """
        func: 用于为测试sheet中的初始化用例和恢复数据用例进行序号编排
        :param cases:
        :return:
        """
        if not cases:
            return []
        no_order_cases = []
        used_order_cased = []
        for case in cases:
            no_order_cases.append(case) if not case.get("order") else used_order_cased.append(case)
        used_order_cased_x = sorted(used_order_cased, key=lambda x: x['order'])
        return used_order_cased_x + no_order_cases

    def _order_for_testcase(self, cases, base_num):
        """
        func：用于给所有测试用例编排执行顺序
        :param cases:
        :return:
        """
        if not cases:
            return []
        orders = self._get_cases_orders(cases)
        log.debug(string.Template("**************$o****************").substitute(o=orders))
        max_num = max(orders)+1 if orders else 1
        ordered = []
        for case in cases:
            try:
                order = int(case['order']) if case['order'] else None
            except Exception as e:
                log.error(string.Template("integer order number error, error info: $e").substitute(e=e))
                order = None
            if order:
                case['order'] = base_num + order
            else:
                case['order'] = base_num + max_num
                max_num += 1
            ordered.append(case)
        return ordered

    @classmethod
    def _get_cases_orders(cls, cases):
        orders = []
        for case in cases:
            if case['order']:
                orders.append(case['order'])
        return orders


class Serialize(object):
    def __init__(self, api_info):
        self.api_info = api_info
        log.info(string.Template("serialize api info is: $api_info").substitute(api_info=self.api_info))

    def serialize(self):
        self.order_fields_check()
        self.params_serialize()
        self.header_serialize()
        self.case_vars_serialize()
        self.interface_var_serialize()
        self.verify_fields_serialize()
        self.restore_serialize()
        self.init_serialize()
        self.dyparam_serialize()
        self.expression_serialize()
        self.method_check()
        self.wait_time_value_check()
        self.url_prepare()
        self.db_verify_serialize()
        return self.api_info

    @classmethod
    def _json_serialize(cls, s):
        try:
            # s = json.dumps(s)
            return ast.literal_eval(s)
        except Exception as e:
            log.error(string.Template("string serialize json fail, source string: $s, error info: $e").substitute(s=s, e=e))
            raise JsonSerializeException("serialize to JSON format error")

    def _init_detail(self):
        for k, v in self.api_info.items():
            if v.strip():
                if not v.startswith('{'):
                    self.api_info[k] = "{" + v
                if not v.endswith('}'):
                    self.api_info[k] = v + '}'

    def order_fields_check(self):
        order = self.api_info['order'] if self.api_info.get("order") else None
        log.info(string.Template("api request order info is: $order").substitute(order=order))
        if not order:
            return None
        try:
            res = int(order)
            self.api_info['order'] = res
            return res
        except Exception as e:
            log.error(string.Template("api order param format error, please input a integer number "
                                      "error info: $e").substitute(e=e))
            raise JsonSerializeException

    def params_serialize(self):
        # params = self.api_info['params'].strip().replace('\n', '')
        params = self.api_info['params'].strip().replace('\n', '') if self.api_info.get("params") else None
        log.info(string.Template("api request params info is: $params").substitute(params=params))
        if not params:
            return
        res = self._json_serialize(params)
        if res:
            self.api_info['params'] = res
            return res
        else:
            log.error(string.Template("api request params format error, params info: $params").substitute(params=self.api_info['params']))
            return False

    def header_serialize(self):
        header = self.api_info['header'].strip().replace('\n', '') if self.api_info.get("header") else None
        log.info(string.Template("api request header info is: $header").substitute(header=header))
        if not header:
            return
        res = self._json_serialize(header)
        if res:
            self.api_info['header'] = res
            return res
        else:
            log.error(string.Template("api request header format error, header info: $header").substitute(
                header=self.api_info['header']))
            return False

    def case_vars_serialize(self):
        case_vars = self.api_info['case_vars'].strip().replace('\n', '') if self.api_info.get("case_vars") else None
        log.info(string.Template("api request case_vars info is: $case_vars").substitute(case_vars=case_vars))
        if not case_vars:
            return
        res = self._json_serialize(case_vars)
        if res:
            self.api_info['case_vars'] = res
            return res
        else:
            log.error(string.Template("api request case_vars format error, case_vars info: $case_vars").substitute(
                _vars=self.api_info['case_vars']))
            return False

    def interface_var_serialize(self):
        var = self.api_info['interface_var'].strip().replace('\n', '') if self.api_info.get("interface_var") else None
        log.info(string.Template("api request interface_var info is: $var").substitute(var=var))
        if not var:
            return
        res = self._json_serialize(var)
        if res:
            self.api_info['interface_var'] = res
            return res
        else:
            log.error(string.Template("api request interface_var format error, interface_var info: $var").substitute(
                var=self.api_info['interface_var']))
            return False

    def verify_fields_serialize(self):
        verify = self.api_info['verify_fields'].strip().replace('\n', '') if self.api_info.get('verify_fields') else None
        log.info(string.Template("api request verify_fields info is: $verify").substitute(verify=verify))
        if not verify:
            return
        res = self._json_serialize(verify)
        if res:
            self.api_info['verify_fields'] = res
            return res
        else:
            log.error(string.Template("api request verify_fields format error, verify_fields info: $verify_fields").substitute(
                verify_fields=self.api_info['verify_fields']))
            return False

    def expression_serialize(self):
        expression = self.api_info['expression'].strip().replace('\n', '') if self.api_info.get('expression') else None
        log.info(string.Template("api request expression info is: $expression").substitute(expression=expression))
        if not expression:
            return
        res = self._json_serialize(expression)
        if res:
            self.api_info['expression'] = res
            return res
        else:
            log.error(
                string.Template("api request expression format error, expression info: $expression").substitute(
                    expression=self.api_info['expression']))
            return False

    def init_serialize(self):
        init = self.api_info['init'].strip().replace('\n', '') if self.api_info.get('init') else None
        log.info(string.Template("api request init info is: $init").substitute(init=init))
        if not init:
            return
        res = self._json_serialize(init)
        srlz_res = []
        if res:
            for case in res:
                sr = Serialize(case)
                sr.url_prepare()
                sr.method_check()
                sr.wait_time_value_check()
                srlz_res.append(sr.api_info)
            self.api_info['init'] = srlz_res
            return srlz_res
        else:
            log.error(
                string.Template("api request init format error, init info: $init").substitute(
                    init=self.api_info['init']))
            return False

    def restore_serialize(self):
        restore = self.api_info['restore'].strip().replace('\n', '') if self.api_info.get('restore') else None
        log.info(string.Template("api request restore info is: $restore").substitute(restore=restore))
        if not restore:
            return
        res = self._json_serialize(restore)
        srlz_res = []
        if res:
            for case in res:
                sr = Serialize(case)
                sr.url_prepare()
                sr.method_check()
                sr.wait_time_value_check()
                srlz_res.append(sr.api_info)
            self.api_info['restore'] = srlz_res
            return srlz_res
        else:
            log.error(
                string.Template("api request restore format error, restore info: $restore").substitute(
                    restore=self.api_info['restore']))
            return False

    def dyparam_serialize(self):
        dyparam = self.api_info['dyparam'].strip().replace('\n', '') if self.api_info.get('dyparam') else None
        log.info(string.Template("api request dyparam info is: $dyparam").substitute(dyparam=dyparam))
        if not dyparam:
            return
        res = self._json_serialize(dyparam)
        if res:
            flag = True
            databases_list = Process.base_configs.get('database') or {}
            error_msg = ""
            for k, v in res.items():
                sql_ = v.get('sql')
                db = v.get('db')
                if not sql_:
                    flag = False
                    error_msg += "{} sql语句不能为空，请检查\n".format(k)
                if not db or db not in databases_list:
                    flag = False
                    error_msg += "{} 配置的db选项没有在基础配置中配置相关的参数\n".format(k)
                else:
                    v['ip'] = databases_list[db].get('ip')
                    v['port'] = databases_list[db].get('port')
                    v['db_type'] = databases_list[db].get('type')
                    v['user'] = databases_list[db].get('user')
                    v['pwd'] = databases_list[db].get('pwd')
                res[k] = v
            if not flag:
                log.error(error_msg)
                raise JsonSerializeException

            self.api_info['dyparam'] = res
            return res
        else:
            log.error(
                string.Template(
                    "api request dyparam format error, dyparam info: $dyparam").substitute(
                    dyparam=self.api_info['dyparam']))
            return False

    def header_manager_serialize(self):
        header_manager = self.api_info['header_manager'].strip().replace('\n', '') if self.api_info.get('header_manager') else None
        log.info(string.Template("api request header_manager info is: $header_manager").substitute(header_manager=header_manager))
        if not header_manager:
            return
        res = self._json_serialize(header_manager)
        if res:
            self.api_info['header_manager'] = res
            return res
        else:
            log.error(
                string.Template("api request header_manager format error, header_manager info: $header_manager").substitute(
                    header_manager=self.api_info['header_manager']))
            return False

    def wait_time_value_check(self):
        wait_time = self.api_info['wait_time'] if self.api_info.get('wait_time') else None
        if isinstance(wait_time, str):
            wait_time = wait_time.strip().replace('\n', '')

        log.info(string.Template("api info wait_time info is: $wait_time").substitute(
            wait_time=wait_time))
        if not wait_time:
            return
        try:
            res = float(wait_time)
            self.api_info['wait_time'] = res
            return res
        except Exception as e:
            log.error(string.Template("wait_time params format error,the wait_time info: $wait_time, "
                                      "error info: $e").substitute(wait_time=wait_time, e=e))
            raise JsonSerializeException

    def method_check(self):
        method = self.api_info['method'].strip().replace('\n', '') if self.api_info.get('method') else None
        log.info(string.Template("api info method info is: $method").substitute(
            method=method))
        supported = ['get', 'post', 'delete', 'put']
        if not method:
            log.error(string.Template("method params are required").substitute())
            raise JsonSerializeException
        elif method.lower() not in supported:
            log.error(string.Template("method params only support $s").substitute(s=supported))
            raise JsonSerializeException
        else:
            self.api_info['method'] = method.upper()
            return method.upper()

    def url_prepare(self):
        url = self.api_info['url'].strip().replace('\n', '') if self.api_info.get('url') else None
        hostname = self.api_info['hostname'].strip().replace('\n', '') if self.api_info.get('hostname') else Process.base_configs.get('hostname')
        log.info(string.Template("api info url info is: $url").substitute(
            url=url))
        if not url:
            log.error(string.Template("url params are required").substitute())
            raise JsonSerializeException
        elif not url.startswith('http://'):
            if not hostname:
                log.error('hostname if empty,please Check that the URL configuration is correct')
                raise JsonSerializeException
            res = hostname + url
            self.api_info['url'] = res
            return res
        else:
            return url

    def db_verify_serialize(self):
        """
        func：对测试用例中的db_verify项进行json格式化和基本字段校验
        首先判断db_verify字段是否符合json格式，如果符合，则该字段进行sql语句判断有无，db配置是否在基础配置中已配置，检查的类型是否正确
        能检查的类型为：= or == 表示查询的值和预期值要相等，~ or ~=表示预期值包含在查询结果中，! or != 表示查询值不能等于预期值，
                     ~ or !~ 表示预期值不能包含在查询值中
        :return:json格式化之后的db_verify字段
        """
        db_verify = self.api_info['db_verify'].strip() if self.api_info.get('db_verify') else None
        log.info(string.Template("api request db_verify info is: $db_verify").substitute(
            db_verify=db_verify))
        if not db_verify:
            return
        res = self._json_serialize(db_verify)
        if res:
            flag = True
            databases_list = Process.base_configs.get('database') or {}
            type_list = ["=", '==', '!', '!=', '~', '~=', '!~', '~!']
            error_msg = ""
            for k, v in res.items():
                sql_ = v.get('sql')
                db = v.get('db')
                type_ = v.get('type') or '='
                if not sql_:
                    flag = False
                    error_msg += "{} sql键不能为空，请检查\n".format(k)
                if not db or db not in databases_list:
                    flag = False
                    error_msg += "{} 配置的db选项没有在基础配置中配置相关的参数\n".format(k)
                else:
                    v['ip'] = databases_list[db].get('ip')
                    v['port'] = databases_list[db].get('port')
                    v['db_type'] = databases_list[db].get('type')
                    v['user'] = databases_list[db].get('user')
                    v['pwd'] = databases_list[db].get('pwd')
                if type_ not in type_list:
                    flag = False
                    error_msg += "{} 配置的type目前无法识别，请检查type选项是否以下选项:{}\n".format(k, type_list)
                res[k] = v
            if not flag:
                log.error(error_msg)
                raise JsonSerializeException

            self.api_info['db_verify'] = res
            return res
        else:
            log.error(
                string.Template(
                    "api request db_verify format error, db_verify info: $db_verify").substitute(
                    db_verify=self.api_info['db_verify']))
            return False

    @classmethod
    def database_config_check(cls, values):
        """
        func:检查基础配置中的database配置是否符合格式
            1. 检查是否能正常格式化为json类型
            2. 检查配置中的ip/port/user/pwd是否已经配置
            3. 检查port是否为全数字
        :param values: 待检查的databases字符
        :return: json后的databases
        """

        res = Serialize._json_serialize(values)
        if not res:
            log.error('databases配置是非法json格式，请检查')
            return False
        for db_name, db_dict in res.items():
            ip = db_dict.get('ip') or db_dict.get('hostname')
            port = db_dict.get('port') or db_dict.get('端口')
            user = db_dict.get('user') or db_dict.get('username')
            pwd = db_dict.get('pwd') or db_dict.get('password') or db_dict.get('passwd')
            if not ip or not port or not user or not pwd:
                log.error('请输入完整的数据库配置，需要包含ip/port/user/pwd')
                return False
            try:
                port = int(port)
                db_dict['port'] = port
                db_dict['ip'] = ip
                db_dict['user'] = user
                db_dict['pwd'] = pwd
            except Exception as e:
                log.error('数据库配置的端口包含非数字字符: 错误信息: {}'.format(e))
                return False
            res[db_name] = db_dict

        return res
