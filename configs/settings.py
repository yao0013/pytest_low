# -*- coding: utf-8 -*-
import os
import logging

current_path = os.path.abspath(os.getcwd())

# 日志配置
log_path = os.path.join(current_path, "logs")
log_devel = "DEBUG"

# 模板用例存放目录
template_file_path = os.path.join(current_path, "static")

# 测试用例存放目录
testcase_file_path = os.path.join(current_path, "testcase")

# 脚本自动生成的用例的存放目录
auto_create_testcase_path = os.path.join(testcase_file_path, "auto_create")

# 旧平台转换后生成的用例的存放目录

old_testcase_file_path = os.path.join(current_path, "testcase")

# 接口测试结果存放目录（Excel保存的文件）
excel_reports_path = os.path.join(current_path, "reports")

# 接口测试结果存放目录（allure生成的测试报告）
allure_reports_path = os.path.join(current_path, "reports")


# Excel用例文件字段对应的列位置
excel_fields = {
    "order": 0,
    "module": 1,
    "casename": 2,
    "description": 3,
    "url": 4,
    "method": 5,
    "params": 6,
    "header": 7,
    "case_vars": 8,
    "interface_var": 9,
    "wait_time": 10,
    "verify_fields": 11,
    "res_text": 12,
    "res_header": 13,
    "status_code": 14,
    "db_verify": 15,
    "expression": 16,
    "res_time": 17,
    "init": 18,
    "restore": 19,
    "dyparam": 20,
    "header_manager": 21,
    "iteration": 22,
    "global_var_key": 0,
    "global_var_value": 1,
    "local_var_key": 0,
    "local_var_value":1
}

fields_mapper = {
    "interface_var": "interface_var",
    "verify_fields": "verify_fields",
    "sql": "sql",
    "expression": "expression",
    "init": "init",
    "restore": "restore",
    "dyparam": "dyparam",
    "header_manager": "header_manager"
}

# 旧平台相关的配置
# 旧平台导出的Excel表，各个字段对应的下标位置
old_platform_fields_mapper = {
    "test_task_key": 0,
    "tc_name": 1,
    "dst": 2,
    "cmd_name": 3,
    "input_params": 4,
    "input_values": 5,
    "order_index": 6,
    "wait_time": 7,
    "expected": 8,
    "max_repeat_time": 9,
    "api_type": 10,
    "description": 11,
    "jsonClient": 12,
    "jsonClientUser": 13
}

url_defalut_prefix = '/api/'

# 测试报告通知相关的配置
# 邮件发送相关的配置
mail_host = "localhost"
mail_server = "mail.cstnet.cn"
mail_port = 994
mail_sender = "lufq@g-cloud.com.cn"
mail_pwd = "Lufo1235639"

# 钉钉机器人配置
dingrobot_token = "https://oapi.dingtalk.com/robot/send?access_token=e4f78376428b13df20e65e152c529acc" \
                  "f8976b2501f0a59282d7f72fdc394410"
dingrobot_keyword = "我是小精灵"  # 发送钉钉消息时，通过关键字的方式设置安全设置，和下方的secret选择其中一种
dingrobot_secret = "SEC5124a1e5cf2510a35aec333f2b6715c57d6f56a5e9def7aa1d7946c53a77c376"  # 通过签名加密的方式设置安全设置


