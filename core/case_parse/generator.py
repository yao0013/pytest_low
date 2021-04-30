# -*- coding: utf-8 -*-

"""
auth: leo
功能： 根据Excel用例表格，自动生成python可执行测试套和测试用例
"""
import os
import shutil
from string import Template
from configs import settings
from core.case_parse.base import Process
from core.logs import log


class Generator(object):
    def __init__(self, task):
        if not isinstance(task, Process):
            raise TypeError("测试用例不是Process的对象，请检查")
        self.testsuites = task.testsuites
        self.init_case = task.init_case
        self.restore_case = task.restore_case
        self.base_dir = settings.template_file_path
        self.testcase_dir = settings.auto_create_testcase_path
        self._testcase_dir_init()
        self.empty_code = """    pass"""

    def _testcase_dir_init(self):
        if os.path.isdir(self.testcase_dir):
            try:
                shutil.rmtree(self.testcase_dir)
            except Exception as e:
                log.error(Template("testcase目录无法删除，请检查是否有其他应用正在使用该目录下的资源，错误信息:$e").substitute(e=e))
                return False
        os.makedirs(self.testcase_dir)
        with open(os.path.join(self.testcase_dir, "__init__.py"), 'w', encoding='utf-8') as f:
            f.write("# -*- coding: utf-8 -*-")

    def generate_testsuite(self):
        for sheet_name, testsuites in self.testsuites.items():
            if not testsuites:
                continue
            init_case = testsuites.get('init_case')
            restore_case = testsuites.get('restore_case')
            testcase = testsuites.get('testcase')
            py_code = ""
            py_code += self._create_header_code()  #读取header_template模板文件
            py_code += self._create_save_interface_vars_code(testsuites['local_vars']) #读取save_interface_vars_template模板文件
            if init_case:
                py_code += self._create_setup_class_case_code(init_case)
            if restore_case:
                py_code += self._create_teardown_class_case_code(restore_case)
            if testcase:
                py_code += self._create_testcase_code(testcase)
            py_code += self._create_testcase_common_func_code()
            with open(os.path.join(self.testcase_dir, "test_{}.py".format(sheet_name)), 'w', encoding='utf-8') as f:
                f.write(py_code)
            log.info(Template("create testsuite files complete").substitute())

    def generate_common_test(self):
        py_code = ""
        py_code += self._create_common_header() #读取 task_common_header_template模板文件
        py_code += self._create_common_init_case_code(self.init_case) #读取task_common_init_case_template模板文件
        py_code += self._create_common_restore_class_code()  #读取task_common_restore_class_template模板文件
        py_code += self._create_common_restore_case_code(self.restore_case) #读取task_common_restore_case_template模板文件
        with open(os.path.join(self.testcase_dir, "test_task_common.py"), 'w', encoding='utf-8') as f:
            f.write(py_code)
        log.info(Template("create common test files complete").substitute())

    def _create_header_code(self):
        return self._read_file("header_template")

    def _create_save_interface_vars_code(self,local_vars):

        code_str= self._read_file("save_interface_vars_template")
        return Template(code_str).substitute(testsuite_localvars=local_vars)

    def _create_testcase_code(self, testsuite):
        if not testsuite:
            return self.empty_code
        code_str = self._read_file("testcase_template")
        replaced = ""
        default_index = 0
        existing = []  # 用来规避测试方法重名

        for tesecase in testsuite:
            order = tesecase['order']
            module = tesecase['module'] if tesecase.get('module') else "--"
            params = tesecase['params']
            casename = "test_{}".format(tesecase['casename']) if tesecase['casename'] else "test_autotest_{}".format(default_index)
            if casename in existing:
                casename = "{}_1".format(casename)
            existing.append(casename)
            description = tesecase['description']
            init_case = tesecase['init'] if tesecase['init'] else []
            restore_case = tesecase['restore'] if tesecase['restore'] else []
            replaced += Template(code_str).substitute(order=order, module=module, casename=casename, description=description,
                                                      testcase=tesecase, init_case=init_case, restore_case=restore_case,
                                                      params=params)
        return replaced

    def _create_setup_class_case_code(self, init_case):
        if not init_case:
            return self.empty_code
        code_str = self._read_file("setup_class_template")
        return Template(code_str).substitute(testsuite_init=init_case)

    def _create_teardown_class_case_code(self, restore_case):
        if not restore_case:
            return self.empty_code
        code_str = self._read_file("teardown_class_template")
        return Template(code_str).substitute(testsuite_restore=restore_case)

    def _create_testcase_common_func_code(self):
        return self._read_file("testcase_common_func_template")

    def _read_file(self, path):
        with open(os.path.join(self.base_dir, path), 'r', encoding='utf-8') as f:
            return f.read()

    def _create_common_header(self):
        return self._read_file("task_common_header_template")

    def _create_common_init_case_code(self, testcases):
        if not testcases:
            return self.empty_code
        code_str = self._read_file("task_common_init_case_template")
        replaced = ""
        default_index = 0
        existing = []  # 用来规避测试方法重名

        for tesecase in testcases:
            order = tesecase['order']
            casename = "test_{}".format(tesecase['casename']) if tesecase['casename'] else "test_task_init_{}".format(
                default_index)
            if casename in existing:
                casename = "{}_1".format(casename)
            existing.append(casename)
            replaced += Template(code_str).substitute(casename=casename, order=order, testcase=tesecase)
        return replaced

    def _create_common_restore_case_code(self, testcases):
        if not testcases:
            return self.empty_code
        code_str = self._read_file("task_common_restore_case_template")
        replaced = ""
        default_index = 0
        existing = []  # 用来规避测试方法重名

        for tesecase in testcases:
            order = tesecase['order']
            casename = "test_{}".format(tesecase['casename']) if tesecase['casename'] else "test_task_restore_{}".format(
                default_index)
            if casename in existing:
                casename = "{}_1".format(casename)
            existing.append(casename)
            replaced += Template(code_str).substitute(casename=casename, order=order, testcase=tesecase)
        return replaced

    def _create_common_restore_class_code(self):
        return self._read_file("task_common_restore_class_template")

