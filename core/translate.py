# -*- coding: utf-8 -*-
"""
author: lufoqin
func: 将旧平台的用例切换到新的平台上运行
    主要步骤：
        1. 读取旧平台的Excel用例
        2. 对url、param进行转换
        3. 补充header和method
        4. 解析用例关联变量
        5. 解析结果匹配功能
        6. 转换为新的接口用例
"""
import re
import sys
from string import Template
import os

from configs import settings
from core.logs import log
from core.utils import ExcelHelper as EH


class Translate(object):

    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.file_name = os.path.split(self.excel_file)[-1]
        self.all_sheets = None
        self.excel_read_helper = EH.ReadHelper(self.excel_file)
        self._read_file()
        self.sheet_case = None
        self.global_var = []

    def _read_file(self):
        """
        读取文件
        :return:
        """
        self.all_sheets = self.excel_read_helper.read_file()

    def _read_row(self, sheet):
        """
        读取sheet内容，根据行进行结果返回，返回的是一个generator
        :param sheet:
        :return:
        """
        return self.excel_read_helper.read_row_content(sheet)

    def parse_case(self):
        """
        对所有用例根据sheetname进行转换
        :return:
        """
        all_sheets = {}
        mapper = settings.excel_fields
        new_excel_file = os.path.join(settings.old_testcase_file_path, "new_{}".format(os.path.split(self.file_name)[-1]))
        excel_helper = CaseWrite(list(self.all_sheets.keys()))
        for sheet_name, sheet in self.all_sheets.items():
            testcases = list(self._read_row(sheet))
            log.debug(Template("testcase: $testcases").substitute(testcases=testcases))
            testcases = self._format(testcases)
            all_sheets[sheet_name] = []
            if testcases:
                self.sheet_case = testcases[1:]
                all_sheets[sheet_name].append(self.testcase_switch())
            for case in self.sheet_case:
                data_list = [""] * 25
                data_list[mapper['order']] = case['order_index'] if case.get('order_index') else ""
                data_list[mapper['casename']] = case['tc_name'] if case.get('tc_name') else ""
                data_list[mapper['description']] = case['description'] if case.get('description') else ""
                data_list[mapper['url']] = case['url'] if case.get('url') else ""
                data_list[mapper['method']] = case['method'] if case.get('method') else ""
                data_list[mapper['params']] = case['params'] if case.get('params') else ""
                data_list[mapper['header']] = case['header'] if case.get('header') else ""
                data_list[mapper['interface_var']] = case['interface_var'] if case.get('interface_var') else ""
                data_list[mapper['wait_time']] = case['wait_time'] if case.get('wait_time') else ""
                data_list[mapper['verify_fields']] = case['verify_fields'] if case.get('verify_fields') else ""
                data_list[mapper['res_text']] = case['res_text'] if case.get('res_text') else ""
                data_list[mapper['module']] = case['test_task_key'] if case.get('test_task_key') else ""
                excel_helper.append(sheet_name, data_list)
        if self.global_var:
            for v in self.global_var:
                excel_helper.append("全局变量", [v])
        excel_helper.save(new_excel_file)
        log.info("旧平台用例转换完毕，转换后的测试用例文件位于：{}".format(new_excel_file))

    def _format(self, testcases):
        json_case = []
        for case in testcases:
            json_case.append(self._read_case_content(case))
        return json_case

    @classmethod
    def _read_case_content(cls, case):
        """
        将用例信息转换为dict格式，对相关的字段进行记录
        :param case:
        :return:
        """
        mapper = settings.old_platform_fields_mapper
        case_info = {}
        case_info['test_task_key'] = case[mapper['test_task_key']].value
        case_info['tc_name'] = case[mapper['tc_name']].value
        case_info['dst'] = case[mapper['dst']].value
        case_info['cmd_name'] = case[mapper['cmd_name']].value
        case_info['input_params'] = case[mapper['input_params']].value
        case_info['input_values'] = case[mapper['input_values']].value
        case_info['order_index'] = case[mapper['order_index']].value
        case_info['wait_time'] = case[mapper['wait_time']].value
        case_info['expected'] = case[mapper['expected']].value
        case_info['max_repeat_time'] = case[mapper['max_repeat_time']].value
        case_info['api_type'] = case[mapper['api_type']].value
        case_info['description'] = case[mapper['description']].value
        case_info['jsonClient'] = case[mapper['jsonClient']].value
        case_info['jsonClientUser'] = case[mapper['jsonClientUser']].value

        return case_info

    def testcase_switch(self):
        """
        根据每个sheet，进行用例转换
        :return:
        """
        testcases = self.sheet_case
        if not testcases:
            return
        for index, case in enumerate(testcases):
            case = self.switch_url(case)
            case = self.add_header(case)
            case = self.add_method(case)
            case = self.switch_params_and_value(case)
            case = self.switch_expected(case)
            self.sheet_case[index] = case

        log.debug(Template("**************************$case").substitute(case=self.sheet_case))

    @classmethod
    def switch_url(cls, case):
        case['url'] = settings.url_defalut_prefix + case['cmd_name'] if case.get('cmd_name') else ""
        return case

    def switch_params_and_value(self, case):
        """
        进行参数转换，分别根据随机参数化规则、引用另一个用例返回结果里的某个值规则、引用另一个用例返回结果里的某个值（附加添加）、全局变量规则进行转换
        :param case:
        :return:
        """
        p_c = re.compile(r'(<#c(\w+)>#(\S+))')  # 引用另一个用例返回结果正则匹配
        p_c_a = re.compile(r'(<#c(\w+)>(.+?=.+?#)(\S+))')  # 引用另一个用户返回结果带附加条件正则匹配
        p_p = re.compile(r'(<#p>(\w+)([\\d]+))')  # 引用随机参数化正则匹配
        p_g = re.compile(r'(<#g(\w+)>)')  # 引用全局变量匹配
        params = str(case['input_params']).split('#,')
        values = str(case['input_values']).split('#,')
        case['params'] = {}
        if len(params) != len(values):
            log.error(Template("用例的输入参数个数和参数值的个数不一致，请检查，用例信息：$case").substitute(case=case))
            sys.exit(-1)
        for index, v in enumerate(values):
            case['params'][params[index]] = v
            p_c_r = re.findall(p_c, v)
            p_c_a_r = re.findall(p_c_a, v)
            p_p_r = re.findall(p_p, v)
            p_g_r = re.findall(p_g, v)
            if p_c_r:
                for item in p_c_r:
                    rpl_str, casename, var_name, var_value = self.parse_c_symbol(item)
                    case['params'][params[index]] = v.replace(rpl_str, "{" + var_name + "}")
                    self.set_interface_var_for_testcase(casename, var_name, var_value)
            if p_c_a_r:
                for item in p_c_a_r:
                    rpl_str, casename, var_name, var_value = self.parse_c_a_symbol(item)
                    case['params'][params[index]] = v.replace(rpl_str, "{" + var_name + "}")
                    self.set_interface_var_for_testcase(casename, var_name, var_value)
            if p_p_r:
                for item in p_p_r:
                    rpl_str, var_value = self.parse_p_symbol(item)
                    case['params'][params[index]] = v.replace(rpl_str, var_value)

            if p_g_r:
                for item in p_g_r:
                    rpl_str, var_name = self.parse_g_symbol(item)
                    case['params'][params[index]] = v.replace(rpl_str, "{" + var_name + "}")
                    self._set_case_global_var(var_name)

        return case

    def switch_expected(self, case):
        """
        进行expected匹配结果转换，如果使用的是=号两边的值对比的是，将结果写入case的verify_fields中，如果只有单个值的，写入case的res_text中
        :param case: 需要处理的用例
        :return:处理后的用例
        """
        expecteds = str(case['expected']).split('#,')
        case['verify_fields'] = {}
        case['res_text'] = ""
        for i, item in enumerate(expecteds):
            result = self.parse_expected(source=item)
            if not result:
                continue
            if not isinstance(result, tuple):
                case['res_text'] += "{},".format(result)
            else:
                exp_key = result[0]
                exp_value = result[1]
                casenames = result[2]
                var_names = result[3]
                var_values = result[4]
                case['verify_fields'][exp_key] = exp_value
                for j in range(0, len(var_names)):
                    self.set_interface_var_for_testcase(casenames[j], var_names[j], var_values[j])
        return case

    @classmethod
    def add_method(cls, case):
        """
        添加默认请求方法
        :param case:
        :return:
        """
        case['method'] = 'post'
        return case

    @classmethod
    def add_header(cls, case):
        """
        添加默认头信息
        :param case:
        :return:
        """
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Auth-Token": "{token}"
        }
        case['header'] = header
        return case

    def parse_c_symbol(self, item):
        """
        对引用另一个用例返回结果里某个值进行参数转换，转换规则：<#c + 用例名称 + ># + 引用的值格式识别，识别到后，提取对应的需要设置接口变量
        的用例名和需要替换的字符，接口变量名、接口变量值。直接将参数引用设置为接口变量名即可
        :param item:
        :return:
        """
        replace_str = item[0]
        casename = item[1]
        var_value = item[2]
        var_name = "{}_{}".format(casename.replace(' ', ''), var_value.replace('/', '_'))
        return replace_str, casename, var_name, var_value

    def parse_c_a_symbol(self, source):
        """
        func：对引用另一个用例返回结果里某个值进行转换（附加条件） 根据<#cDescribeNodeNetcards>/data/netcardUsageCn=G-Cloud
        管理通道#/data/netcardId 格式进行变量识别，识别到了之后，将在需要引用的用例
        的地方，进行接口变量设置，参数直接使用接口变量引入的方式进行替换
        :param source:
        :return:需要替换的字符，需要设置接口变量的用例名，接口变量名，接口变量值
        """
        replace_str = source[0]
        casename = source[1]
        eqa = source[2]
        var_value = source[3]
        eqa_list = re.findall(r'((/\w+)=([^/]+))', eqa)
        for item in eqa_list:
            if re.match(r'^\d+$', item[2]):  # 判断是否只有数字，如果全部是数字的话，需要使用``扩起来，不是全部数字的使用''扩起来
                rpl_str = "[?{}==`{}`]".format(item[1].strip('/'), item[2].strip('/'))
            else:
                rpl_str = "[?{}=='{}']".format(item[1].strip('/'), item[2].strip('/'))
            eqa = eqa.replace(item[0], rpl_str)
        var_value = eqa.lstrip('/').replace('/', '.') + "." + var_value.split('/')[-1]
        var_name = "{}_{}".format(casename.replace(' ', ''), var_value.replace('/', '_'))
        return replace_str, casename, var_name, var_value

    @classmethod
    def parse_g_symbol(cls, source):
        """
        func：对参数化引用的全局变量进行转换，转换规则为，识别到全局变量后，对全局变量加{}标识
        :param source:
        :return:
        """
        rpl_str = source[0]
        var_name = source[1]
        return rpl_str, var_name

    @classmethod
    def parse_expected(cls, source):
        """
        结果匹配规则转换
        例子：
        1. /success=true#,/data/userMaxPwdErrorNum=5
        2. /success=true#,/data/netcardName=[<#cAddPoolNetcard>#/data/netcardName]
        3. /success=true#,/data/data/instanceId=[<#cRunInstanceWLL>#/data/instanceId]#/data/data/state=Running
        4. /<#eRequestId>
        思路：先将最复杂的结果找出，进行规则替换：引用其他用例里的值（附加条件）正则匹配规则，将引用附加条件的
        :param source:
        :return: expected的值，expected的键，需要设置的变量名，需要设置的变量值
        """
        p_o_e = re.compile(r'<#e(\w+)>$')  # 只有单个键，没有需要检验的值正则匹配规则，上述例子中的4情况
        p_e_a = re.compile(r'(/([^=/]+)=\[*(<#c(\w+)>#/(.+?))*#)')  # 引用其他用例里的值（附加条件）正则匹配规则，上述例子中的3
        p_a = re.compile(r'(/([^=/]+)=(\[*(<#c(\w+)>#/(.+))))')  # 引用其他用例里的值正则匹配规则，上述例子中的2
        p_f = re.compile(r'.+\](/.+?)=')  # 上述两种规则替换后，将结果取值部分替换掉，对应上述例子3中的/data/data/state，替换后剩余.state
        p_split = re.compile(r'(.+)={1}(.+)')  # 进行最终=号两边的取值，左边对应expected的键，右边对应expected的值
        var_names = []
        var_values = []
        casenames = []
        source = source.strip()
        p1 = re.findall(p_e_a, source)
        if p1:
            log.info("expected 符合 引用其他用例里的值（附加条件）")
            p1 = p1[0]
            casename = p1[3]
            var_name = casename + "_" + p1[4].replace('/', '_').strip(']')
            var_value = p1[4].replace('/', '.').strip(']')
            rpl_str = "[?{}=='{}']".format(p1[1], "{" + var_name + "}")
            source = source.replace(p1[0], rpl_str)
            casenames.append(casename)
            var_names.append(var_name)
            var_values.append(var_value)
        p2 = re.findall(p_a, source)
        if p2:
            log.info("expected 符合 引用其他用例里的值")
            p2 = p2[0]
            casename = p2[4]
            var_name = casename + "_" + p2[5].replace('/', '_').strip(']')
            var_value = p2[5].replace('/', '.').strip(']')
            rpl_str = "{" + var_name + "}"
            source = source.replace(p2[2], rpl_str)
            casenames.append(casename)
            var_names.append(var_name)
            var_values.append(var_value)
        p3 = re.findall(p_f, source)
        if p3:
            for i in p3:
                source = source.replace(i, "." + i.split('/')[-1])

        source = source.lstrip('/').replace('/', '.')  # 对剩余/符号进行.号替换
        if re.match(p_o_e, source):
            p4 = re.findall(p_o_e, source)
            return p4[0]
        else:
            p5 = re.findall(p_split, source)
            if p5:
                return p5[0][0], p5[0][1], casenames, var_names, var_values
            else:
                log.error(Template("expected表达式不符合已知的规则，请检查，expected信息：$s").substitute(s=source))
                return False

    def parse_reg_symbol(self, case, result, testcases):
        pass

    def parse_d_symbol(self, case, result, testcases):
        pass

    @classmethod
    def parse_p_symbol(cls, source):
        """
        对引用随机参数化参数进行转换，转换规则为，匹配到<#p> + 命名 + 参数化位数格式后，对命名的左右添加$符号
        :param source:
        :return:
        """
        rpl_str = source[0]
        var_value = source[1]
        var_value = "${}$".format(var_value)
        return rpl_str, var_value

    def set_interface_var_for_testcase(self, casename, var_name, var_value):
        """
        func: 设置用例的接口变量，根据传入的用例名、变量名和变量值进行接口变量设置
        :param casename: 用例名
        :param var_name: 变量名
        :param var_value: 变量值
        :return: 设置了接口变量之后的用例
        """
        testcases = self.sheet_case
        backup = testcases
        var_value = var_value.strip('/').replace('/', '.')
        for i, case in enumerate(testcases):
            if case['tc_name'] == casename:
                if not case.get('interface_var'):
                    case['interface_var'] = {}
                case['interface_var'][var_name] = var_value
                self.sheet_case[i] = case
                backup[i] = case
        return backup

    def _set_case_global_var(self, var_name):
        """
        func：设置当前测试用例需要的全局变量名，以供用例解析完后，人为在全局变量处添加对应的值
        :param var_name:
        :return:
        """
        if var_name not in self.global_var:
            self.global_var.append(var_name)


class CaseWrite(EH.WriteHelper):
    def __init__(self, sheet_names):
        super(CaseWrite, self).__init__()
        self.set_title("global_var")
        self.set_title("base_config")
        for sheet in sheet_names:
            self.set_title("test_case", sheet)

    def set_title(self, sheet_type, sheet_name="test_case"):
        if sheet_type == "global_var":
            title = ["变量名", "变量值", "说明"]
            self.append("全局变量", title)
            self.set_sheet_info(sheet_name, row=1, col=0)
        elif sheet_type == "base_config":
            title = ["配置项", "配置值"]
            self.append("基础配置", title)
            self.set_sheet_info(sheet_name, row=1, col=0)
        elif sheet_type == "test_case":
            title = ["order", "module", "casename", "description", "url", "method", "params", "header", "case_vars",
                     "interface_var", "wait_time", "verify_fields", "res_text", "res_header", "status_code", "sql",
                     "value", "expression", "time", "init", "restore", "dyparam", "header_manager", "database", "iteration"]

            self.write_merge(sheet_name, 1, 1, 0, 24, "接口测试")
            self.write_merge(sheet_name, 2, 2, 0, 8, "接口信息")
            self.write(sheet_name, 2, 8, "用例变量")
            self.write(sheet_name, 2, 9, "接口变量")
            self.write(sheet_name, 2, 10, "等待时间")
            self.write(sheet_name, 2, 11, "校验字段")
            self.write(sheet_name, 2, 12, "响应内容")
            self.write(sheet_name, 2, 13, "响应头")
            self.write(sheet_name, 2, 14, "状态码")
            self.write_merge(sheet_name, 2, 2, 15, 16, "数据库校验")
            self.write(sheet_name, 2, 17, "表达式校验")
            self.write(sheet_name, 2, 18, "响应时间（单位秒）")
            self.write(sheet_name, 2, 19, "初始化")
            self.write(sheet_name, 2, 20, "恢复")
            self.write(sheet_name, 2, 21, "动态参数")
            self.write(sheet_name, 2, 22, "信息头管理")
            self.write(sheet_name, 2, 23, "数据库")
            self.write(sheet_name, 2, 24, "迭代次数")
            self.set_sheet_info(sheet_name, row=3, col=0)
            self.append(sheet_name, title)

        else:
            log.error('sheet type is not supported, the sheet type is: {}'.format(sheet_type))
            raise ValueError('sheet type is not supported, the sheet type is: {}'.format(sheet_type))


