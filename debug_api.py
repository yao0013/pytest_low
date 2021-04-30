# -*- coding: utf-8 -*-
"""
author：lufoqin
func：api调试器，通过使用命令行命令：python debug_api.py -f file_path 传入api调试信息
    api文件编写规则：1. 可以使用单个json格式传入单个api调试信息；2. 可以使用[]列表形式，传入多个api调试信息
    举例：以下例子保存在api_info.txt文件中，通过命令行启动调试：python debug_api.py -f ./api_info.txt
        文件中具有两个api调试信息，每个大{}括号内具有一个完整的api信息
    [
        {
            "url": "http://192.168.203.38/api/gce/namespace/page",
            "method": "post",
            "params": {
                    "pageNumber": 1,
                    "limit": 10,
                    "clusterId": "710b6a72-870f-4326-8579-cabb00148167",
                    "detail": "true"
                },
            "header": {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Auth-Token": "60a930a8-fc3b-3df7-93a7-0f17aa369d50",
                    "x-gce-tenant-id":"40e92db1-5153-43ad-be33-a92999ea5f9a"

                },
            "verify_fields": {
                "requestId": "123456"
            },
            "res_text": "data[0].id,data[0].name",
            "status_code": 200,
            "res_time": 2,
            "expression": "len(response['data'])>1"
        },
        {
            "url": "http://192.168.203.38/api/gce/namespace/page",
            "method": "post",
            "params": {
                    "pageNumber": 1,
                    "limit": 10,
                    "clusterId": "710b6a72-870f-4326-8579-cabb00148167",
                    "detail": "true"
                },
            "header": {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Auth-Token": "60a930a8-fc3b-3df7-93a7-0f17aa369d50",
                    "x-gce-tenant-id":"40e92db1-5153-43ad-be33-a92999ea5f9a"

                },
            "verify_fields": {
                "requestId": "123456"
            },
            "res_text": "data[0].id,data[0].name",
            "status_code": 200,
            "res_time": 2,
            "expression": "len(response['data'])>1"
        }
    ]
"""
import argparse
import os

from core.api_debugger import Debugger


if __name__ == "__main__":
    usage = """
    -f --file api调试文件路径
    """
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', help="api调试文件路径")
    parse = args.parse_args()
    api_info = {
        "file": os.path.abspath(parse.file)
    }
    Debugger(**api_info).api_request()


