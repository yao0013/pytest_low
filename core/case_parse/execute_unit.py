# -*- coding: utf-8 -*-
import random
import string
import re
import json
import jmespath
import pytz
from datetime import datetime, timedelta

from core.logs import log
from core.CustomExceptions import TestcaseTypeErrorException, VarReplaceException
from core.databases.db_helper import DbHelper
from string import Template


def generate_random_str(lenght=16):
    """
    func: 生成随机字符串
    :param lenght: 字符串的长度
    :return: 随机字符串
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(lenght))


class VarReplace(object):
    def __init__(self, case, object_list):
        self.case = case
        self.object_list = object_list
        self.backup_case = case
        self.interface_vars = {}

    def var_replace(self):
        self.case = var_add_random_str(self.case)
        self._var_replace()
        log.info(Template("变量替换后的用例信息:$case").substitute(case=self.case))
        return self.case

    def _var_replace(self):
        """
        功能：解析测试用例中是否存在需要变量替换的字符串
        流程：根据传入的用例和需要检查的对象列表，判断对象列表中是否包含有用例中需要转换的变量字符串，如果有，则将对应的字符串转换为对应的变量值
        """
        case = self.case
        object_list = self.object_list
        if not isinstance(case, dict):
            raise TestcaseTypeErrorException()
        if not isinstance(object_list, list):
            raise TypeError("object list is not a list object")
        self._add_interface_vars()
        object_list.append(self)
        pattern_front = re.compile(r"@{")
        pattern_back = re.compile(r"@}")
        random_front = generate_random_str()
        random_back = generate_random_str()
        try:
            content = json.dumps(case, ensure_ascii=False)
        except Exception as e:
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            raise VarReplaceException
        content = re.sub(pattern_front, random_front, content)
        content = re.sub(pattern_back, random_back, content)
        # log.debug(string.Template("after replaced random string: $content").substitute(content=content))
        pattern = re.compile(r"\{\w+\}")
        key_words = re.findall(pattern, content)
        log.debug(string.Template("所有需要进行变量替换的变量为: $key_words").substitute(key_words=key_words))

        if key_words:
            """
            循环遍历所有待替换的字符，如果待替换的字符在传入的对象列表中有对应的属性，则进行替换
            否则不作处理
            对象替换按传入的对象的下标进行排序，匹配到了之后，退出循环，即取最先匹配到的对象的属性值
            """
            for key_word in key_words:
                real_word = key_word.lstrip('{').rstrip('}')
                for index in range(0, len(object_list)):
                    log.debug(Template("$o对象的interface_vars属性$a").substitute(o=object_list[index].__class__.__name__,
                                                                a=object_list[index].__dict__.get('interface_vars')))
                    if not hasattr(object_list[index], "interface_vars"):
                        log.debug(Template("$o对象没有interface_vars属性").substitute(o=object_list[index]))
                        continue
                    attr_dict = object_list[index].__dict__
                    interface_var_dict = attr_dict["interface_vars"]  # 获取对象的所有属性值
                    if real_word in interface_var_dict:
                        log.debug(Template("正在替换变量：$s").substitute(s=real_word))
                        content = content.replace(key_word, str(interface_var_dict[real_word]))
                        break

        content = content.replace(random_front, r'{')
        content = content.replace(random_back, r'}')
        try:
            json_content = json.loads(content)
            self.case = json_content
        except Exception as e:
            log.error(string.Template("testcase json loads fail, the error info: $e").substitute(e=e))
            raise VarReplaceException

    def _add_interface_vars(self):
        case = self.case
        params = case['params']
        header = case['header']
        if params:
            for k, v in params.items():
                self.interface_vars[k] = v
        if header:
            for k, v in header.items():
                self.interface_vars[k] = v


def var_add_random_str(case):
    case = case
    if not isinstance(case, dict):
        raise TestcaseTypeErrorException()

    pattern_random = re.compile(r"@$")
    random_str = generate_random_str()
    try:
        content = json.dumps(case, ensure_ascii=False)
    except Exception as e:
        log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
        raise VarReplaceException
    content = re.sub(pattern_random, random_str, content)
    # log.debug(string.Template("after replaced random string: $content").substitute(content=content))
    pattern = re.compile(r"\$\S+\$")
    key_words = re.findall(pattern, content)
    log.debug(string.Template("所有需要添加随机字符的变量为: $key_words").substitute(key_words=key_words))

    if key_words:
        """
        循环遍历所有待替换的字符，如果待替换的字符在传入的对象列表中有对应的属性，则进行替换
        否则不作处理
        对象替换按传入的对象的下标进行排序，匹配到了之后，退出循环，即取最先匹配到的对象的属性值
        """
        for key_word in key_words:
            real_word = key_word.lstrip('$').rstrip('$')

            log.debug(Template("正在替换变量：$s").substitute(s=real_word))
            content = content.replace(key_word, real_word+generate_random_str(8))

    content = content.replace(random_str, r'$')
    try:
        return json.loads(content)
    except Exception as e:
        log.error(string.Template("testcase json loads fail, the error info: $e").substitute(e=e))
        raise VarReplaceException


def parse_case_vars(case, var_object: object):
    if not isinstance(case, dict):
        return 'testcase is not a dict object'
    if not hasattr(var_object, "interface_vars"):
        var_object.interface_vars = {}
    case_var = case.get('case_vars')
    if case_var:
        for k, v in case_var.items():
            var_object.interface_vars[k] = v


def parse_interface_var(source: object, response: object) -> object:
    var_dict = {}
    if not isinstance(source, dict):
        return 'response is not a dict'
    for k, v in source.items():
        try:
            res = jmespath.search(v, response)
            if isinstance(res, list):
                var_dict[k] = res[0]
            else:
                var_dict[k] = res
        except Exception as e:
            log.error(string.Template("get interface_var:$v from response fail,error info: $e").substitute(v=v, e=e))
    return var_dict


def datetime_translate(case):
    """
    将用例中符合日期格式的变量替换成对应的时间日期
    :param case: 需要处理的用例
    :return: 处理后的用例
    """
    case = case
    time_format = "%Y-%m-%d %H:%M:%S"
    if not isinstance(case, dict):
        raise TestcaseTypeErrorException()
    pattern_now = re.compile(r'<#dnow\(\)>')
    pattern_now_add = re.compile(r'(<#dnow\(\)\+(\d+)>)')
    pattern_date = re.compile(r'(<#d(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2}:\d{2})>)')
    pattern_date_add = re.compile(r'(<#d(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2}:\d{2})\+(\d+)>)')
    try:
        content = json.dumps(case, ensure_ascii=False)
    except Exception as e:
        log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
        raise VarReplaceException
    key_words_now = re.findall(pattern_now, content)
    key_words_now_add = re.findall(pattern_now_add, content)
    key_words_date = re.findall(pattern_date, content)
    key_words_date_add = re.findall(pattern_date_add, content)
    now_time = datetime.now(tz=pytz.timezone("Asia/Shanghai"))
    now_time_str = datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime(time_format)
    if key_words_now:
        log.debug("时间替换：<#dnow()> ----> {}".format(now_time_str))
        content = content.replace(r'<#dnow()>', now_time_str)
    if key_words_now_add:
        for key_word in key_words_now_add:
            _time = now_time + timedelta(minutes=float(key_word[1]))
            log.debug("时间替换：{} ----> {}".format(key_word[0], _time.strftime(time_format)))
            content = content.replace(key_word[0], _time.strftime(time_format))
    if key_words_date:
        for key_word in key_words_date:
            log.debug("时间替换：{} ----> {}".format(key_word[0], key_word[1]))
            content = content.replace(key_word[0], key_word[1])
    if key_words_date_add:
        for key_word in key_words_date_add:
            try:
                _datetime = datetime.strptime(key_word[1], time_format)
            except Exception as e:
                log.error("时间字符串无法转换为strptime，请检查时间是否符合规范，默认转换为当前时间，错误信息:{}".format(str(e)))
                _datetime = now_time
            add_time = _datetime + timedelta(minutes=float(key_word[2]))
            log.debug("时间替换：{} ----> {}".format(key_word[0], add_time.strftime(time_format)))
            content = content.replace(key_word[0], add_time.strftime(time_format))
    try:
        return json.loads(content)
    except Exception as e:
        log.error("testcase json loads fail, the error info: {}".format(str(e)))
        raise VarReplaceException


def dyparam_parse(testcase: dict, var_object: object):
    """
    func: 根据dyparam里的sql信息，进行数据库查询，将查询到的结果存入var_object对象的interface_vars属性中
    :param dyparam: 测试用例中的dyparam信息经过json转换后的内容
    :param var_object: 用于存放测试sheet接口变量的对象
    :return: 添加了从数据库中查询出来的值之后的var_object对象
    """
    if not isinstance(testcase, dict):
        return "testcase is not a dict"
    dyparam = testcase.get('dyparam')
    if not dyparam:
        return None
    if not isinstance(dyparam, dict):
        return "dyparam is not a dict type"
    if not hasattr(var_object, "interface_vars"):
        var_object.interface_vars = {}
    log.info('进入dyparam解析')
    for name_, sql_info in dyparam.items():
        ip = sql_info.get('ip')
        port = sql_info.get('port')
        pwd = sql_info.get('pwd')
        user = sql_info.get('user')
        db_type = sql_info.get('db_type')
        values = sql_info.get('values')
        sql = sql_info.get('sql')
        rs = DbHelper().query(ip=ip, port=port, user=user, pwd=pwd, db_type=db_type, sql=sql)
        if not rs:
            log.warning("sql: {} 查询结果为空".format(sql))
            for var_name, reslut_key in values.items():
                var_object.interface_vars[var_name] = ""
            continue

        rs = rs[0]
        try:
            for var_name, reslut_key in values.items():
                log.info('添加interface_var: {}={}'.format(var_name, rs.get(reslut_key)))
                var_object.interface_vars[var_name] = rs.get(reslut_key)
        except Exception as e:
            log.error('add interface_vars fail, error info is: {}'.format(e))
            return False
    return var_object


def check_verify_fields(fields, response):
    error_info = ""
    if not fields:
        return error_info
    if not isinstance(fields, dict):
        return "params type error，verify fields is not a dict"

    def json_compare(k, v, r):
        info = ""
        try:
            # if str(v) != str(eval("response" + k)):
            if str(v) != str(jmespath.search(k, r)):
                info += Template("response $k not equal $v, real value is: "
                                       "$response").substitute(k=k, v=v, response=str(jmespath.search(k, r)))
        except Exception as e:
            info += Template("对比结果$k时出现异常，异常信息:$e").substitute(k=k, e=e)
        return info

    def reg_compare(k, v, r):
        info = ""
        v = v.lstrip('<#reg>')
        res = jmespath.search(k, r)
        log.debug(Template("*************$res*************").substitute(res=res))
        try:
            if not re.match(v, res):
                info += "响应结果使用正则表达式匹配失败，请检查，"
        except Exception as e:
            info += Template("响应结果使用正则表达式匹配异常，异常信息：$e").substitute(e=e)
        return info

    for k, v in fields.items():
        if v.startswith('<#reg>'):
            error_info += reg_compare(k, v, response)
        else:
            error_info += json_compare(k, v, response)
    return error_info


def check_response_text(fields, response):
    error_info = ""
    log.debug(Template("fields: $fields, response: $response").substitute(fields=fields, response=response))
    if not fields:
        return error_info
    if isinstance(fields, str):
        log.debug('is a string fields, value is:'.format(fields))
        fs = fields.split(',')
    elif isinstance(fields, list):
        log.debug('is a list fields, value is: '.format(str(fields)))
        fs = fields
    else:
        log.error('fields param type error')
        return 'check res_text error, fields param type error'
    for text in fs:
        text = text.lstrip("'").lstrip('"').rstrip("'").rstrip('"')
        if text:
            log.debug(Template("待校验的内容: $text").substitute(text=text))
            if isinstance(response, dict):
                isempty = jmespath.search(text, response)
                if isempty is None:
                    error_info += Template("接口响应内容没有待校验的字段:$t，响应内容:$res").substitute(t=text, res=response)
            else:
                if text not in response:
                    error_info += Template("接口响应内容没有待校验的字段:$t，响应内容:$res").substitute(t=text, res=response)

    return error_info


def check_response_header(fields, headers):
    error_info = ""
    if not fields:
        return error_info
    log.debug(Template("fields: $fields, headers: $headers").substitute(fields=fields, headers=headers))
    if not fields:
        return error_info
    if isinstance(fields, str):
        log.debug('is a string fields, value is:'.format(fields))
        fs = fields.split(',')
    elif isinstance(fields, list):
        log.debug('is a list fields, value is: '.format(str(fields)))
        fs = fields
    else:
        log.error('fields param type error')
        raise TypeError('fields param type error')
    for text in fs:
        text = text.lstrip("'").lstrip('"').rstrip("'").rstrip('"')
        if text:
            if isinstance(headers, dict):
                # if not headers.get(text):
                isempty = jmespath.search(text, headers)
                if isempty is None:
                    error_info += Template("接口响应内容没有待校验的字段:$t，响应内容:$res").substitute(t=text, res=headers)
            else:
                if text not in headers:
                    error_info += Template("接口响应内容没有待校验的字段:$t，响应内容:$res").substitute(t=text, res=headers)

    return error_info


def check_status_code(code, response):
    error_info = ""
    if not code:
        return error_info
    try:
        code = int(code)
    except Exception as e:
        log.error(Template("接口响应状态码入参错误，请检查, 入参值：$code").substitute(code=code))
        error_info += Template("接口响应状态码入参错误，请检查, 入参值：$code").substitute(code=code)
        return error_info
    if code != response:
        error_info += Template("接口响应码校验失败:预期值：$n，响应值:$res").substitute(n=code, res=response)
    return error_info


def check_response_time(_time, response):
    error_info = ""
    if not _time:
        return error_info
    try:
        _time = float(_time)
        if _time < response:
            log.error(Template("接口响应时间超时，期望值: $t， 响应值: $r").substitute(t=_time, r=response))
            error_info += Template("接口响应时间超时，期望值: $t， 响应值: $r").substitute(t=_time, r=response)
            return error_info
    except Exception as e:
        log.error(Template("接口响应时间入参错误，请检查: $t").substitute(t=_time))
        error_info += Template("接口响应时间入参错误，请检查: $t").substitute(t=_time)
        return error_info


def check_pyexpression(pys, response):
    error_info = ""
    response = response
    exe_pys = []
    if not pys:
        return error_info
    if isinstance(pys, list):
        exe_pys = pys
    elif isinstance(pys, str):
        exe_pys.append(pys)
    else:
        error_info += "py表达式入参错误，参数仅支持列表和字符串格式"
        return error_info
    for py in exe_pys:
        try:
            if not eval(py):
                log.error(Template("py表达式执行失败，表达式内容：$py").substitute(py=py))
                error_info += (Template("py表达式执行失败，表达式内容：$py").substitute(py=py))
        except Exception as e:
            error_info += Template("执行py表达式异常，表达式内容：$py, 异常信息：$e").substitute(py=py, e=e)

    return error_info


def check_db_verify(sql_info):
    if not isinstance(sql_info, dict):
        return '数据库验证失败，sql_info 入参类型错误，请传入dict类型'
    error_info = ""

    for check_name, sql_dict in sql_info.items():
        type_ = sql_dict.get('type') or '='
        ip = sql_dict.get('ip')
        port = sql_dict.get('port')
        pwd = sql_dict.get('pwd')
        user = sql_dict.get('user')
        db_type = sql_dict.get('db_type')
        check_values = sql_dict.get('check') or {}
        sql = sql_dict.get('sql')
        rs = DbHelper().query(ip=ip, port=port, user=user, pwd=pwd, db_type=db_type, sql=sql)
        if not rs:
            error_info += "sql: {} 查询结果为空".format(sql)
            continue

        if type_ == "=" or type_ == "==":
            rs = rs[0]
            for k, v in check_values.items():
                if str(rs.get(k)) != str(v):
                    log.error("数据库验证失败，预期结果：{}等于{}, 查询结果：{}".format(k, v, rs))
                    error_info += "数据库验证失败，预期结果：{}等于{}, 查询结果：{}\n".format(k, v, rs)
        elif type_ == "!" or type_ == "!=":
            rs = rs[0]
            for k, v in check_values.items():
                if str(rs.get(k)) == str(v):
                    log.error("数据库验证失败，预期结果：{}不等于{}, 查询结果：{}".format(k, v, rs))
                    error_info += "数据库验证失败，预期结果：{}不等于{}, 查询结果：{}\n".format(k, v, rs)

        elif type_ == "~" or type_ == "~=":
            for k, v in check_values.items():
                flag = False
                for r in rs:
                    if str(r[k]) == str(v):
                        flag = True
                        break
                if not flag:
                    log.error('数据库验证失败，预期值：{}包含{},查询结果:{}'.format(k, v, rs))
                    error_info += '数据库验证失败，预期值：{}包含{},查询结果:{}\n'.format(k, v, rs)

        elif type_ == "!~" or type_ == "~!":
            for k, v in check_values.items():
                flag = True
                for r in rs:
                    if str(r[k]) == str(v):
                        flag = False
                        break
                if not flag:
                    log.error('数据库验证失败，预期值：{}不包含{},查询结果:{}'.format(k, v, rs))
                    error_info += '数据库验证失败，预期值：{}不包含{},查询结果:{}\n'.format(k, v, rs)
        else:
            log.error('数据库验证类型不支持，请检查')
            error_info += "数据库验证类型不支持，请检查"

    return error_info

