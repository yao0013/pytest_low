# -*- coding: utf-8 -*-
"""
测试结果保存到Excel中和自动生成allure测试报告并开启allure测试报告服务
"""
import os
import re
import subprocess
import sys
import time
import chardet
import pytz
from datetime import datetime
from configs import settings
from core.logs import log
from core.utils.ExcelHelper import WriteHelper
import shutil
import ast


class ResultSave(WriteHelper):
    def __init__(self):
        super(ResultSave, self).__init__()
        self.sheet_title = ["casename", "url", "method", "params", "header", "response", "status_code", "response_time"]

    def append_row(self, sheet_name, data_list, passed):
        """
        往Excel表格中追加数据
        :param sheet_name:
        :param data_list:
        :param passed 用例是否执行通过
        :return:
        """
        passed = passed or 'PASS'
        if not isinstance(data_list, list):
            log.error("要写入的结果的入参类型错误")
            return False
        if sheet_name not in self.sheet_info:
            self.append(sheet_name, self.sheet_title)
        else:
            self.sheet = self.workbook.get_sheet(sheet_name)

        if passed.upper() == 'PASS':
            style = self.set_style('green')
        elif passed.upper() == 'FAIL':
            style = self.set_style('red')
        elif passed.upper() == 'WARNING':
            style = self.set_style('yellow')
        else:
            style = self.set_style('green')
        self.append(sheet_name, data_list, style)


RS = ResultSave()


class AllureReport(object):
    def __init__(self):
        self.allure_report = "allure_report"
        self.categories_trend_file_name = "categories-trend.json"
        self.duration_trend_file_name = "duration-trend.json"
        self.history_file_name = "history.json"
        self.history_trend_file_name = "history-trend.json"
        self.retry_trend_file_name = "retry-trend.json"

    def open_report_server(self, report_dir, ip=None, port=None):
        if not port:
            port = 55555
        suffix_dir = os.path.split(report_dir)[0]
        relative_path = os.path.split(report_dir)[1]
        self.trend_detail(report_dir)
        os.chdir(suffix_dir)
        self.check_port_is_open(port)
        generate_cmd = "allure generate {} -o {} -c".format(relative_path, self.allure_report)
        if ip:
            open_server_cmd = "allure open {} -h {} -p {}".format(self.allure_report, ip, port)
        else:
            open_server_cmd = "allure open {} -p {}".format(self.allure_report, port)
        obj = subprocess.Popen(generate_cmd, shell=True)
        obj.communicate()
        obj = subprocess.Popen(open_server_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        couter = 0
        for item in iter(obj.stdout.readline, 'b'):
            couter += 1
            encode_type = chardet.detect(item)
            if encode_type['encoding'] == 'utf-8':
                item = item.decode('utf-8')
            elif encode_type['encoding'] == 'Windows-1252':
                item = item.decode('Window-1252')
            else:
                pass
            log.debug('subprocess out is: {}'.format(str(item)))
            pattern = re.compile(r'Server started at <(.+?)>\.')
            rs = re.search(pattern, str(item))
            if rs:
                url = rs.group(1)
                log.info('reports server is: {}'.format(url))
                return url
            time.sleep(0.5)
            if couter > 100:
                return "获取allure报告服务地址失败"

    def check_port_is_open(self, port):
        sys_plat = sys.platform.lower()
        if "linux" in sys_plat:
            self.kill_process_by_port_on_linux(port)
        else:
            self.kill_process_by_port_on_win(port)

    @classmethod
    def kill_process_by_port_on_win(cls, port):
        find_cmd = 'netstat -aon|findstr "{}"'.format(port)
        kill_cmd = "taskkill -pid {} -f"
        with os.popen(find_cmd) as res:
            res = res.read().split('\n')
        for line in res:
            temp = [i for i in line.split(' ') if i != '']
            log.debug('the netstat info is: {}'.format(temp))
            if len(temp) > 4:
                addr = temp[1]
                if str(addr.split(':')[1]) == str(port):
                    pid = temp[4]
                    log.info('find the port, the corresponding PID is: {}, and kill the PID process'.format(pid))
                    os.system(kill_cmd.format(pid))
                    return
        log.info('No corresponding port process was found')
        return

    @classmethod
    def kill_process_by_port_on_linux(cls, port):
        '''kill -9 $(netstat -nlp | grep :''' + str(
            port) + ''' | awk '{print $7}' | awk -F"/" '{ print $1 }')
        '''

        find_cmd = "netstat -nlp |grep :" + str(port) + "|awk '{print $7}' |awk -F '/' {print $1}"
        kill_cmd = "kill -9 {}"
        with os.popen(find_cmd) as res:
            pid = res.read().strip()
        if pid:
            log.info('find the port, the corresponding PID is: {}, and kill them'.format(pid))
            os.system(kill_cmd.format(pid))
            return
        else:
            log.info('No corresponding port process was found')
            return

    @classmethod
    def _check_encoding(cls, item):
        encode_type = chardet.detect(item)
        if encode_type['encoding'] == 'utf-8':
            return item.decode('utf-8')
        elif encode_type['encoding'] == 'Windows-1252':
            return item.decode('Window-1252')
        else:
            return item

    def trend_detail(self, report_dir):
        log.info('处理allure测试报告trend内容')
        if not os.path.isdir(report_dir):
            log.error('需要处理trend的目录不是一个有效路径，请检查')
            return False
        allure_json_file_dirs = []  # 所有allure json报告的所有目录
        suffix_dir = os.path.split(report_dir)[0]  # 测试报告路径前缀
        relative_path = os.path.split(report_dir)[1]  # 当前测试报告目录
        for item in os.listdir(suffix_dir):
            if re.match(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', item):
                allure_json_file_dirs.append(item)

        allure_json_file_dirs = sorted(allure_json_file_dirs, reverse=True)
        log.info('all the allure report dirs is: {}'.format(allure_json_file_dirs))

        last_allure_report_dir = os.path.join(suffix_dir, self.allure_report)  # 最近一次allure json报告的目录
        log.info('last_allure_report_dir is: {}'.format(last_allure_report_dir))
        if not os.path.isdir(last_allure_report_dir):
            log.info('no last_allure_report_dir, no need to detail trend')
            return None
        else:
            last_allure_report_history_dir = os.path.join(last_allure_report_dir, "history")  # 最近一次allure_report目录中的history目录
            last_allure_json_dir = os.path.join(suffix_dir, allure_json_file_dirs[0])  # 最近一次allure json文件目录
            last_history_dir = os.path.join(last_allure_json_dir, "history")  #最近一次allure json文件目录中history目录

            self.manual_join_trend_file(last_allure_report_history_dir, last_history_dir, report_dir)

    def manual_join_trend_file(self, result_dir, allure_json_dir, dst_dir):

        if not os.path.isdir(allure_json_dir):  # 如果allure json目录中没有history目录，则只要把allure_report中的history copy到需要生成allure 报告的目录中即可
            log.info('copy file, the source dir is: {}, dst dir is: {}'.format(result_dir, dst_dir))
            os.makedirs(allure_json_dir)
            os.chdir(result_dir)
            shutil.copy(self.categories_trend_file_name, allure_json_dir)
            shutil.copy(self.duration_trend_file_name, allure_json_dir)
            shutil.copy(self.history_trend_file_name, allure_json_dir)
            shutil.copy(self.history_file_name, allure_json_dir)
            shutil.copy(self.retry_trend_file_name, allure_json_dir)
        else:
            log.info('read the json file content')
            result_categories_content = self._read_json_file(os.path.join(result_dir, self.categories_trend_file_name))
            results_duration_content = self._read_json_file(os.path.join(result_dir, self.duration_trend_file_name))
            results_history_trend_content = self._read_json_file(os.path.join(result_dir, self.history_trend_file_name))
            results_retry_content = self._read_json_file(os.path.join(result_dir, self.retry_trend_file_name))

            #  上一次allure json目录中的history文件内容
            allure_categories_content = self._read_json_file(os.path.join(allure_json_dir, self.categories_trend_file_name))
            allure_duration_content = self._read_json_file(os.path.join(allure_json_dir, self.duration_trend_file_name))
            allure_history_trend_content = self._read_json_file(os.path.join(allure_json_dir, self.history_trend_file_name))
            allure_retry_content = self._read_json_file(os.path.join(allure_json_dir, self.retry_trend_file_name))
            allure_history_content = self._read_json_file(os.path.join(allure_json_dir, self.history_file_name))

            #  内容拼接
            allure_categories_content.append(result_categories_content[0])
            allure_duration_content.append(results_duration_content[0])
            allure_history_trend_content.append(results_history_trend_content[0])
            allure_retry_content.append(results_retry_content[0])

            # 写入待生成测试报告的目录中
            dst_history_dir = os.path.join(dst_dir, "history")
            if not os.path.isdir(dst_history_dir):
                os.makedirs(dst_history_dir)
            log.info('write new history content to {}'.format(dst_history_dir))
            self._write_json_file(os.path.join(dst_history_dir, self.categories_trend_file_name), allure_categories_content)
            self._write_json_file(os.path.join(dst_history_dir, self.duration_trend_file_name), allure_duration_content)
            self._write_json_file(os.path.join(dst_history_dir, self.history_trend_file_name), allure_history_trend_content)
            self._write_json_file(os.path.join(dst_history_dir, self.retry_trend_file_name), allure_retry_content)
            self._write_json_file(os.path.join(dst_history_dir, self.history_file_name), allure_history_content)

    @classmethod
    def _read_json_file(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ast.parse(content)

    @classmethod
    def _write_json_file(cls, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(content))
