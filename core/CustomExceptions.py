# -*- coding: utf-8 -*-


class JsonSerializeException(Exception):
    def __str__(self):
        print("Api fields parse json fail")


class RequestMethodException(Exception):
    def __str__(self):
        msg = "api request method not supported, The following types of request methods are supported: " \
              "get/post/put/delete/patch"
        print(msg)
        return msg

    def __init__(self, err="api request method not supported"):
        Exception.__init__(self, err)


class ResponseJsonException(Exception):
    def __str__(self):
        msg = "serialize api response to json format fail"
        print(msg)
        return msg

    def __init__(self, err="serialize api response to json format fail"):
        Exception.__init__(self, err)


class TestcaseTypeErrorException(Exception):
    def __str__(self):
        msg = "testcase type is not a dict type"
        print(msg)
        return msg

    def __init__(self, err="testcase type is not a dict type"):
        Exception.__init__(self, err)


class ObjectTypeErrorException(Exception):
    def __str__(self):
        msg = "need to compare object type error"
        print(msg)
        return msg

    def __init__(self, err="need to compare object type error"):
        Exception.__init__(self, err)


class VarReplaceException(Exception):
    def __str__(self):
        msg = "testcase var replace fail"
        print(msg)
        return msg

    def __init__(self, err="testcase var replace fail"):
        Exception.__init__(self, err)


