# -*- coding: utf-8 -*-
"""
author:lufoqin
func: 用于测试结果的消息通知，目前支持邮件通知和钉钉机器人通知
"""
import json
import os
import smtplib
import sys
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from configs import settings
from core.logs import log
from core.case_parse.base import Process


class MailHandler(object):
    """
    func: 邮件发送功能，通过使用send方法发送邮件
    """
    def __init__(self, host=settings.mail_host, server=settings.mail_server, port=settings.mail_port,
                 sender=settings.mail_sender, pwd=settings.mail_pwd):
        self.host = host
        self.server = server
        self.port = port
        self.sender = sender
        self.pwd = pwd
        self.smtp_handler = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.smtp_handler:
            self.close()

    def smtp_link(self):
        """
        func: 连接smtp服务器，判断当前所在的平台，连接smtp服务
        :return:
        """

        if "win" in sys.platform.lower():
            log.info('mail server in windows platform')
            smtp = smtplib.SMTP_SSL(self.server)
        elif "linux" in sys.platform.lower():
            log.info('mail server in linux platform')
            smtp = smtplib.SMTP_SSL(self.server)
        else:
            log.error('mail server not support this system platform')
            raise SystemError('mail server not support this system platform')
        try:
            smtp.connect(self.server, self.port)
            log.info('smtp connect server success')
            smtp.login(self.sender, self.pwd)
            log.info('login mail server success')
            self.smtp_handler = smtp
            return smtp
        except Exception as e:
            log.error('login mail server fail, error info is: {}'.format(e))
            return False

    def send(self, mail_body, receivers, attachs=None, subject="auto-test mail notify"):
        """
        func: 发送邮件功能
        :param mail_body: 邮件文本主体，字符串类型
        :param receivers: 接收者列表，list类型
        :param attachs: 需要添加的附件，list类型，list中的每个元素需要是dict类型，并且需要有filename和filepath两个属性
        :param subject: 邮件主题
        :return:
        """
        if not attachs:
            if not isinstance(attachs, list):
                log.error('attach param is not a list')
                attach = None
        msg = MIMEMultipart()  # 支持邮件中附带附件
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = Header(self.sender, 'utf-8')
        for receiver in receivers:
            msg['To'] = Header(receiver, 'utf-8')

        mail_body = "(本邮件是程序自动下发的，请勿回复！)\r\n" + mail_body
        text_content = MIMEText(mail_body, 'plain', 'utf-8')
        msg.attach(text_content)
        # 添加附件
        if attachs:
            attachs = self.attach_check(attachs)
            for att in attachs:
                filepath = att.get('filepath')
                filename = att.get('filename')
                log.debug('filepath is: {}'.format(filepath))
                att_tmp = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
                att_tmp['Content-type'] = 'application/octet-stream'
                att_tmp['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                msg.attach(att_tmp)
        try:
            if self.smtp_link():
                self.smtp_handler.sendmail(self.sender, receivers, msg.as_string())
                log.info("send mail success!")

        except Exception as e:
            log.error("发送邮件异常, 错误信息：{}".format(e))

    @classmethod
    def attach_check(cls, attachs):
        """
        func：检查附件的格式是否符合要求，举例：[{"filename":"test.jpg", "filepath":"/root/test.jpg"}]
        :param attachs:
        :return:
        """
        checked = []
        if not isinstance(attachs, list):
            log.error('attach param is not a list')
            return False
        for att in attachs:
            if att:
                if not isinstance(att, dict):
                    log.error('attach content is not a dict object')
                    continue
                if att.get("filename") and att.get("filepath") and os.path.isfile(att.get('filepath')):
                    checked.append(att)
                else:
                    log.error('Attachment parameters have no file name or file path or file not found')
        return checked

    def close(self):
        log.info('close smtp')
        self.smtp_handler.quit()


class DingRobotSender(object):

    def __init__(self, token=settings.dingrobot_token):
        self.token = token
        self.default_msg = "大家好，我是钉钉机器人，正在测试，请忽略"

    @classmethod
    def _secret(cls):
        timestamp = str(round(time.time() * 1000))
        secret = settings.dingrobot_secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        log.debug('dingrobot secret timestamp is: {}, sign is: {}'.format(timestamp, sign))
        return timestamp, sign

    def send_text(self, msg, ats=None):
        """
        func: 发送钉钉群消息
        :param msg: text message conntent
        :param ats: phone list of to @, element "all" equal to @all
        :return:
        """
        timestamp, sign = self._secret()
        url_ = self.token
        url_ = url_ + "&timestamp={}&sign={}".format(timestamp, sign)
        log.debug('dingrobot complete url is: {}'.format(url_))
        if ats is None:
            ats = []
        text_msg = {
            "msgtype": "text",
            "text": {
                "content": msg
            }
        }

        at_info = {"atMobiles": [], "isAtAll": False}
        for item in ats:
            if item == "all":
                at_info["isAtAll"] = True
            elif isinstance(item, int):
                at_info["atMobiles"].append(item)
            else:
                pass
        text_msg["at"] = at_info
        header = {
            "Content-Type": "application/json"
        }
        with requests.post(url_, json.dumps(text_msg), headers=header) as res:
            log.info('dingrobot response is: {}'.format(res.text))


class MsgNotify(object):
    passed = 0
    failed = 0
    xfailed = 0
    skipped = 0
    duration = 0
    count = 0

    def __init__(self):
        pass

    @classmethod
    def set_testresult(cls, *args, **kwargs):
        cls.passed = kwargs.get('passed') or 0
        cls.failed = kwargs.get('failed') or 0
        cls.xfailed = kwargs.get('xfailed') or 0
        cls.skipped = kwargs.get('skipped') or 0
        cls.duration = kwargs.get('duration') or 0
        cls.count = kwargs.get('count') or 0

    @classmethod
    def send_mail(cls, mail_body, receivers=None, attachs=None, subject=None):
        if not receivers:
            receivers = Process.base_configs['mail_receivers']
        if not subject:
            subject = "自动化测试通知"
        with MailHandler() as mailhd:
            mailhd.send(mail_body, receivers, attachs, subject=subject)

    @classmethod
    def send_ding_msg(cls, msg, ats=None):
        if not isinstance(ats, list):
            log.error('ats param is not a list')
            ats = []
        if msg:
            DingRobotSender().send_text(msg, ats)

    def send_reports(self, report_text, excel_file_path):
        mail_switch = Process.base_configs['mail_switch']
        dingrobot_switch = Process.base_configs['dingrobot_switch']
        test_results_text = """
本次测试结果汇总：\n用例总数: {}\npassed: {}\nfailed: {}\nxfailed: {}\nskipped: {}\n耗时: {} 秒
""".format(self.count, self.passed, self.failed, self.xfailed, self.skipped, self.duration)
        report_text += test_results_text
        if mail_switch:
            attach = [{"filename": os.path.split(excel_file_path)[1], "filepath": excel_file_path}]
            self.send_mail(report_text, attachs=attach)
        if dingrobot_switch:
            self.send_ding_msg(report_text)
