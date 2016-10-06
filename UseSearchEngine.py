# -*- coding:utf-8 -*-
import sys
import argparse
from commons import Output
from commons import URL
from searchengine import Query
from searchengine import Baidu
from searchengine import Bing
from searchengine import Google
from searchengine import SearchEngineError

def handleException(func):
    '''
    异常处理
        函数修饰器，用于集中异常处理
    '''
    def _wrapper(args):
        try:
            out = Output()
            return func(args, out)
        except PenError as error:
            out.error(str(error))
        except SearchEngineError as error:
            out.error(str(error))
        except KeyboardInterrupt:
            out.error(u"强制退出")
        finally:
            out.close()
    return _wrapper

@handleException
def doGoogleHacking(args, out):
    '''
    Google Hacking功能
    '''
    out.init(u"Google Hacking功能", args.output)

    keywords = args.keywords.decode(sys.stdin.encoding)
    engineName = args.engine.lower().strip() if args.engine else "baidu"
    size = args.size if args.size else 20

    if engineName == "baidu":
        engine = Baidu()
    elif engineName == "bing":
        engine = Bing()
    elif engineName == "google":
        engine = Google()
    else:
        out.error(u"不支持 '{0}' 搜索引擎，必须为 baidu/bing/google 之一".format(engineName))
        return False

    hostSet = set()
    out.warnning(u"'{0}' 在 '{1}' 中的搜索结果如下:\n".format(keywords, engineName))
    for item in engine.search(keywords,size):
        if not args.unique:
            out.info(out.Y("{0:>6} : ".format("title")) + item.title)
            out.info(out.Y("{0:>6} : ".format("url")) + item.url + "\n")
            out.writeLine(item.url)
        else:
            host = URL.getHost(item.url)
            if host:
                if host not in hostSet:
                    hostSet.add(host)
                    out.info(out.Y("{0:>6} : ".format("title")) + item.title)
                    out.info(out.Y("{0:>6} : ".format("url")) + item.url + "\n")
                    out.writeLine(item.url)
                else:
                    continue

def main():
    reload(sys)
    sys.setdefaultencoding("utf8")

    parser = argparse.ArgumentParser(description=u"搜索引擎")
    subparser = parser.add_subparsers(title=u"子命令", description=u"下面为可以使用的子命令，使用 'python UseSearchEngine.py 子命令 -h' 获得子命令帮助")

    #GoogleHacking
    gh = subparser.add_parser("search", help=u"GoogleHacking工具")
    gh.add_argument("keywords", help=u"指定搜索关键字，windows下引号通过两个引号转义特殊字符")
    gh.add_argument("-e", "--engine", help=u"指定搜索引擎，目前支持baidu/bing/google，默认使用baidu")
    gh.add_argument("-s", "--size", type=int, help=u"指定搜索返回条目数，默认为200条")
    gh.add_argument("-o", "--output", help=u"指定输出文件，输出文件为URL列表")
    gh.add_argument("--unique", action="store_true", help=u"设置domain唯一")
    gh.set_defaults(func=doGoogleHacking)

    args = parser.parse_args()
    args.func(args)

if __name__=='__main__':
    #使用方法:python UseSearchEngine.py search  MichealJackson
    main()







    
