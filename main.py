# -*- coding: utf-8 -*-
import os
import sys

import pytest
import pytz
import argparse
from configs import settings
from datetime import datetime
from core.case_parse.base import Process
from core.case_parse.generator import Generator
from core.logs import log
from core.translate import Translate
from core.results import RS, AllureReport
from core.message_notify import MsgNotify


def run_exec(filepath):
    start_time = datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.split(filepath)[1].rstrip('.xls').rstrip('.xlsx')  # 测试用例名，后续保存测试结果需要用到
    testsuites = Process(filepath=filepath)
    gn = Generator(testsuites)
    gn.generate_common_test()
    gn.generate_testsuite()
    now_time = datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S")
    #  测试报告路径默认在report/[测试文件名]/里，文件名以当时的时间为名字
    allure_report_dir = os.path.join(settings.allure_reports_path, filename, now_time)
    excel_report_file = os.path.join(settings.excel_reports_path, filename, "Excel", now_time + ".xls")
    pytest.main(["./testcase", "-v", "-s", "--alluredir={}".format(allure_report_dir)])  # pytest的启动入口
    excel_report_file = RS.save(excel_report_file)  # 保存测试结果到Excel文件
    server_url = AllureReport().open_report_server(allure_report_dir)  # 生成allure测试报告，并打开报告服务
    end_time = datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S")
    report_text = """测试开始时间: {}\n测试结束时间: {}\n测试用例文件名: {}\n测试报告保存路径:\n    Excel: {},\n   allure: {}\n测试报告服务地址: {}\n
""".format(start_time, end_time, os.path.split(filepath)[1], os.path.split(excel_report_file)[1],
               os.path.split(allure_report_dir)[1], server_url)
    MsgNotify().send_reports(report_text, excel_report_file)  # 根据Excel中的配置，发送钉钉消息和邮件通知


def run_translate(filepath):
    """
    解析旧平台用例的入口
    :param filepath: 文件路径
    :return: 处理完后，会在日志结尾处提示新生成的新用例的路径
    """
    Translate(filepath).parse_case()


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', help='excel file path', required=True)  # 需要处理的excel文件
    #  进行处理的类型：old：转换旧平台的用例，new：执行新平台的用例，默认为new
    args.add_argument('-t', '--type', help='old or new. --old platform testcase,will convert to the new platform '
                                           'testcase;  --new: Generate test cases using Excel files and execute them.'
                                           'default:new')

    parse = args.parse_args()
    file_path = os.path.abspath(parse.file)
    type_ = parse.type if parse.type else "new"
    if type_ == "new":
        run_exec(file_path)
    elif type_ == "old":
        run_translate(file_path)
    else:
        log.error("the arg of type is invalid, only support 'new' or 'old'")
        print("the arg of type is invalid, only support 'new' or 'old'")
        sys.exit(-1)

