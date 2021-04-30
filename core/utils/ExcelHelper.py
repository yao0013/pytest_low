# -*- coding: utf-8 -*-
"""
author:lufoqin
func:使用xlwr和xlrd库，封装Excel文件的常用读和写操作
"""
import os
from datetime import datetime
from string import Template
import pytz
import xlwt
import xlrd
from xlwt import Style
from configs import settings
from core.logs import log


class ReadHelper(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.all_sheets = {}

    def read_file(self, filepath=None):
        if not filepath:
            filepath = self.filepath
        all_sheets = {}
        try:
            workbook = xlrd.open_workbook(filepath)
        except Exception as e:
            log.error("open file fail, please check! error info: {}".format(str(e)))
            return False

        sheet_names = workbook.sheet_names()
        log.debug(Template("all the sheet: $sheet").substitute(sheet=sheet_names))
        for sheet in sheet_names:
            all_sheets[sheet] = workbook.sheet_by_name(sheet)
        self.all_sheets = all_sheets
        return all_sheets

    @classmethod
    def read_row_content(cls, sheet):
        try:
            return sheet.get_rows()
        except Exception as e:
            log.error("get sheet rows fail, sheet is: {}".format(sheet.name))
            log.exception(e)


class WriteHelper(object):
    def __init__(self):
        self.sheet = None
        self.sheet_info = {}
        self._init_workbook()

    def _init_workbook(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')

    def write(self, sheet_name, row, col, label, stype=Style.default_style):
        if not isinstance(sheet_name, str) and not isinstance(label, str):
            log.error("要写入的结果的入参类型错误")
            return False
        self._init_sheet(sheet_name)
        log.info('写入数据信息：{}，{}，{}，{}'.format(sheet_name, row, col, label))
        self.sheet.write(row, col, label, stype)

    def write_row(self, sheet_name, start_row, start_col, data_list, style=xlwt.Style.default_style):
        if not isinstance(sheet_name, str) and not isinstance(data_list, list):
            log.error("要写入的结果的入参类型错误")
            return False

        self._init_sheet(sheet_name)
        log.info('写入行数据信息：{}, {}, {}, {}'.format(sheet_name, start_row, start_col, str(data_list)))
        for col, data in enumerate(data_list):
            try:
                data = str(data)
            except Exception as e:
                log.error(Template("待写入的数据无法格式化为string格式，写入异常：$e").substitute(e=e))
                data = "format error"
            self.sheet.write(start_row, start_col+col, data, style)

    def append(self, sheet_name, data_list, style=Style.default_style):
        """
        往Excel表格中追加数据
        :param sheet_name:
        :param data_list:
        :param style 单元格样式
        :return:
        """
        if not isinstance(data_list, list):
            log.error("要写入的结果的入参类型错误")
            return False
        self._init_sheet(sheet_name)
        row = self.sheet_info[sheet_name]['row']
        col = self.sheet_info[sheet_name]['col']

        try:
            self.write_row(sheet_name, row, col, data_list, style)
        except Exception as e:
            log.error(Template("往Excel表格中写入数据异常,异常信息：$e").substitute(e=e))
            return False
        self.sheet_info[sheet_name]['row'] += 1

    def write_merge(self, sheet_name, start_row, end_row, start_col, end_col, label, style=Style.default_style):
        if not isinstance(label, str):
            log.error("要写入的数据入参错误，请传入string类型数据")
            return False
        self._init_sheet(sheet_name)
        log.info('合并单元格写入数据信息：{}, {}, {}, {}, {}, {}'.format(sheet_name, start_row, end_row, start_col, end_col, label))
        try:
            self.sheet.write_merge(start_row, end_row, start_col, end_col, label, style)
            return True
        except Exception as e:
            log.error("往Excel表格中写入合并单元格异常，数据信息：sheet_name: {}, start_row:{}, end_row: {}, start_col: {}, end_col: {},"
                      " label:  {}, 异常信息：{}".format(sheet_name, start_row, end_row, start_col, end_col, label, str(e)))
            return False

    def _init_sheet(self, sheet_name):
        if sheet_name not in self.sheet_info:
            log.info('sheet_info no this sheet_name: {}'.format(sheet_name))
            self.sheet = self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
            self.sheet_info[sheet_name] = {'row': 0, 'col': 0}
        else:
            log.info('sheet_info hava this is sheet_name: {}'.format(sheet_name))
            self.sheet = self.workbook.get_sheet(sheet_name)
        return self.sheet

    def set_sheet_info(self, sheet_name, **kwargs):
        log.info('set sheet_info, args is: {}'.format(str(kwargs)))
        try:
            for k, v in kwargs.items():
                self.sheet_info[sheet_name][k] = v
        except Exception as e:
            log.error("设置sheet_info异常，入参信息: {}, 异常信息：{}".format(str(kwargs), str(e)))

    def save(self, file_name):
        file_name = file_name
        file_dir = os.path.split(file_name)[0]
        if not os.path.isdir(file_dir):
            try:
                os.makedirs(file_dir)
            except Exception as e:
                log.error('create {} folder fail, error info is: {}'.format(file_dir, e))
                return False
        try:
            self.workbook.save(file_name)
        except Exception as e:
            log.error('保存测试结果异常，异常信息：{}'.format(e))
            return "save excel test report failed "
        log.info('file save successfully, file path is: {}'.format(file_name))
        return file_name

    @classmethod
    def set_style(cls, color):
        style = Style.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = pattern.SOLID_PATTERN
        if color == 'red':
            pattern.pattern_fore_colour = Style.colour_map['red']
        elif color == 'green':
            pattern.pattern_fore_colour = Style.colour_map['green']
        elif color == 'yellow':
            pattern.pattern_fore_colour = Style.colour_map['yellow']
        style.pattern = pattern
        return style

