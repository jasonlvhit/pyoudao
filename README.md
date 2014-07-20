## pyoudao 一个简单的命令行查词工具
--------

pyoudao分为两部分，在线查询和本地查询，本地查询支持的没有网络条件下进行简单的英文单词查询，本地词库大约有10万条单词，基本覆盖常用的英文单词。

在线部分使用有道词典的API，查询的功能略微好一点，可以查询整句，和多国语言的汉语含义。

### usage
输入pyoudao或者pyoudao -h，会给出使用帮助和说明：
``` bash
jason:~ pyoudao -h
usage: pyoudao.py [-h] [-o [ONLINE [ONLINE ...]]] [-l [LOCAL [LOCAL ...]]]

Tiny command line tool for youdao translation.

optional arguments:
  -h, --help            show this help message and exit
  -o [ONLINE [ONLINE ...]], --online [ONLINE [ONLINE ...]]
                        online translation
  -l [LOCAL [LOCAL ...]], --local [LOCAL [LOCAL ...]]
                        offline translation, for a given english word, return
                        the chinese meaning
```
简单来说，只有两条命令，在线和离线：

```-o``` 选项使用在线查询：

``` bash
~: pyoudao -o your query
```

```-l``` 选项使用本地查询
``` bash
~: pyoudao -l queryword
```

如下：

``` bash
jason:~ pyoudao -o hello world
==========pyoudao===========
查询: hello world
翻译: 你好,世界
-------------------
基本释义:
你好世界
-------------------

网络释义
----------------------:
关键词: hello world
释义: 你好世界,举个例子,开始
关键词: Hello   World
释义: 会写的人多了去了
关键词: Hello Kitty World
释义: 凯蒂猫气球世界
```

``` bash
jason～: pyoudao -l hello 
================pyoudao===============
查询: o
释义: int.喂,哈罗

======================================

```

Be happy.
