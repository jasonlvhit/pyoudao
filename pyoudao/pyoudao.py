# -*- coding: utf-8 -*-
import argparse
import json
import requests

BASE_URL = "http://fanyi.youdao.com/openapi.do"

Y_VERSION = "1.1"
TYPE = "data"
DOCTYPE = "json"
KEYFROM = "pyoudao"
KEY = "108579965"


class pyoudaoException(Exception):

    errorCode = {0: "正常",
                 20: "要翻译的文本过长",
                 30: "无法进行有效的翻译",
                 40: "不支持的语言类型",
                 50: "无效的key",
                 60: "无词典结果，仅在获取词典结果生效"}

    def __init__(self, code):
        assert code in (self.errorCode.keys())
        self.value = self.errorCode[code]

    def __repr__(self):
        return 'pyoudao execption : %s'% self.value


def request(q):
    params = {"version": Y_VERSION,
              "type": TYPE,
              "doctype": DOCTYPE,
              "keyfrom": KEYFROM,
              "key": KEY,
              "q": q}
    try:
        res = requests.get(BASE_URL, params=params).json()
    except requests.exceptions.RequestsException as e:
        print(e.message)

    return res


def show(res):
    if res['errorCode'] != 0:
        raise pyoudaoException(res['errorCode'])

    print("==========pyoudao===========")
    print("查询:"),
    print(res['query'])
    print("翻译:"),
    print(','.join(res['translation']))
    print("-------------------")

    if 'basic' not in res:
        return

    print("基本释义:")
    for i in res['basic']['explains']:
        print(i)

    print("-------------------")
    if 'phonetic' in res['basic']:
        print("标准发音:"),
        print(res['basic']['phonetic'])
        print("美式发音:"),
        print(res['basic']['us-phonetic'])
        print("英式发音:"),
        print(res['basic']['uk-phonetic'])

    if not res['web']:
        return
    print("\n网络释义\n----------------------:")
    for i in res['web']:
        print("关键词:"),
        print(i['key'])
        print("释义:"),
        print(','.join(i['value']))
    print("\n\n")


def pretty_print(f):
    print(json.dumps(f, sort_keys=True,
                     indent=4, separators=(',', ':')))


def get_parser():
    parser = argparse.ArgumentParser(
        description='Tiny command line tool for youdao translation.')
    parser.add_argument('-t', '--fanyi', type=str, nargs='*',
                        help='translate the keywords or text')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    show(request(' '.join(args['fanyi'])))
    return

if __name__ == "__main__":
    command_line_runner()
