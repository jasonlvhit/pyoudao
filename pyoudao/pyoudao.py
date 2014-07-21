#-*- coding: utf-8 -*-
import argparse
import json
import requests

BASE_URL = "http://fanyi.youdao.com/openapi.do"

Y_VERSION = "1.1"
TYPE = "data"
DOCTYPE = "json"
KEYFROM = "pyoudao"
KEY = "108579965"

# number of child of each trie node
R = 128


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
        return 'pyoudao execption : %s' % self.value

"""
在线部分，使用有道词典的API
online part of pyoudao, using the youdao dict online API
"""


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
    """show the result, and ...i try to make it look better...
    """
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
    """pretty print the json result returned from the youdao API
    """
    print(json.dumps(f, sort_keys=True,
                     indent=4, separators=(',', ':')))

"""
Local dict part, en --> ch, using the trie tree for quick search.
本地部分， 英文单词翻译为中文
本地有大概10万条单词，使用Trie树快速查找
"""

# Trie tree for local dict search


class TrieNode:

    """Trie Node for save the interpretion of word and
    """

    def __init__(self, inter=""):
        self.child = [None for i in range(R)]
        self.inter = inter  # interpretion


def insertTrie(root, word, inter):
    """insert a node into the trie tree which root is param root
    """
    # print(word, inter)
    strlen = len(word)
    if not strlen:
        return

    index = ord(word[0])
    if strlen > 1:
        if not root.child[index]:
            root.child[index] = TrieNode()
        insertTrie(root.child[index], word[1:], inter)
    else:
        if root.child[index]:
            root.child[index].inter = inter
            return
        else:
            root.child[index] = TrieNode(inter)


def createTrie(f):
    root = TrieNode()
    inter_flag = False
    word = ""
    with open(f, 'r') as file:
        for line in file:
            if inter_flag:
                insertTrie(root, word, line)
                inter_flag = False
                continue
            word = line
            inter_flag = True

    return root


def queryTrie(root, word):
    if len(word) == 0 or root == None:
        print("未找到结果")
        return

    index = ord(word[0])
    if len(word) == 1:
        if root.child[index].child[ord('\n')] != None and root.child[index].child[ord('\n')].inter != "":
            print("================pyoudao===============")
            print("查询:"),
            print(word)
            print("释义:"),
            print(root.child[index].child[ord('\n')].inter)
            print("======================================")
            return
        else:
            print("未找到结果")
            return
    else:
        queryTrie(root.child[index], word[1:])


def localQuery(word):
    word = word.strip().lower()
    if(not word[0].isalpha()):
        raise pyoudaoException("invalid local query word")

    root = createTrie("data/" + word[0])
    # print(root.child[ord('a')].child[ord('\n')].inter)
    queryTrie(root, word)
    # localshow(res)

"""
command line parser:

"""


def get_parser():
    parser = argparse.ArgumentParser(
        description='Tiny command line tool for youdao translation.')
    parser.add_argument(
        '-o', '--online', type=str, nargs='*', help='online translation')
    parser.add_argument('-l', '--local', type=str, nargs='*',
                        help='offline translation, for the given english word, return the chinese meaning')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['online'] != None:
        show(request(' '.join(args['online'])))
    elif args['local'] != None:
        localQuery(args['local'][0])
    else:
        print("type the:\n pyoudao -h \nfor the usage or help")
    # show(request(' '.join(args['fanyi'])))
    # return


if __name__ == "__main__":
    command_line_runner()
