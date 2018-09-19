#! /usr/bin/env python

import extargsparse
import sys
import os
import logging
import re

def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    if logging.root is not None and logging.root.handlers is not None and len(logging.root.handlers) > 0:
        logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return

def __get_bash_string_file(infile):
    s = ''
    logging.info('open file [%s] for string'%(infile))
    with open(infile,'rb')  as fin:
        for l in fin:
            if sys.version[0] == '3' and 'b' in fin.mode:
                l = l.decode('utf-8')
            curs = ''
            for c in l:
                if c == '$':
                    curs += '\\'
                    curs += '$'
                elif c == '\\':
                    curs += '\\\\'
                elif c == '`':
                    curs += '\\'
                    curs += '`'
                else:
                    curs += c
            s += curs
            logging.info('[%s] => [%s]'%(l,curs))
    #logging.info('[%s] (%s)'%(infile,s))
    return s

def get_bash_string(args):
    s = ''
    for c in args.subnargs:
        s += __get_bash_string_file(c)
    return s

def replace_string(args,repls):
    fin = sys.stdin
    fout = sys.stdout
    if args.input is not None:
        fin = open(args.input,'rb')
    if args.output is not None:
        fout = open(args.output,'w+b')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        chgstr = l.replace(args.pattern,repls)
        if sys.version[0] == '3' and 'b' in fout.mode:
            fout.write(chgstr.encode('utf-8'))
        else:
            fout.write('%s'%(chgstr))
    if fin != sys.stdin:
        fin.close()
    fin = None
    if fout != sys.stdout:
        fout.close()
    fout = None
    return

def out_string(args,repls):
    fout = sys.stdout
    if args.output is not None:
        fout = open(args.output,'w+b')

    fout.write('%s'%(repls))

    if fout != sys.stdout:
        fout.close()
    fout = None
    return

def __get_insert_string_file(infile):
    s = ''
    i = 0
    logging.info('open [%s] for insert string'%(infile))
    with open(infile,'rb') as fin:
        i = 0
        for l in fin:
            if sys.version[0] == '3' and 'b' in fin.mode:
                l = l.decode('utf-8')
            i += 1
            if i == 1 and l.startswith('#!'):
                continue
            s += l
    logging.info('[%s] (%s)'%(infile,s))
    return s

def get_insert_string(args):
    s = ''
    for f in args.subnargs:
        s += __get_insert_string_file(f)
    return s

def bashinsert_handler(args,parser):
    set_log_level(args)
    repls = get_insert_string(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def bashstring_handler(args,parser):
    set_log_level(args)
    repls = get_bash_string(args)
    replace_string(args,repls)
    sys.exit(0)
    return





def __get_make_python(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\r':
                s += '\\\\'
                s += 'r'
            elif c == '\n':
                s += '\\\\'
                s += 'n'
            elif c == '\t':
                s += '\\\\'
                s += 't'
            elif c == '\\':
                s += '\\\\\\\\'
            elif c == '\'':
                s += '\\\\\''
            elif c == '"':
                s += '\\"'
            elif c == '$':
                s += '\\$$'
            elif c == '`':
                s += '\\'
                s += '`'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s


def get_make_python(args):
    s = ''
    for infile in args.subnargs:
        s += __get_make_python(args,infile)
    return s

def makepython_handler(args,parser):
    set_log_level(args)
    repls = get_make_python(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_make_perl(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '#':
                s += '\\'
                s += '#'
            elif c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '$'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '@':
                s += '\\'
                s += '@'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_make_perl(args):
    s = ''
    for infile in args.subnargs:
        s += __get_make_perl(args,infile)
    return s

def makeperl_handler(args,parser):
    set_log_level(args)
    repls = get_make_perl(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_sh_perl(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '#':
                s += '\\'
                s += '#'
            elif c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '@':
                s += '\\'
                s += '@'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_sh_perl(args):
    s = ''
    for infile in args.subnargs:
        s += __get_sh_perl(args,infile)
    return s

def shperl_handler(args,parser):
    set_log_level(args)
    repls = get_sh_perl(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_sh_python(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '\'':
                s += '\\\\'
                s += '\''
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_sh_python(args):
    s = ''
    for infile in args.subnargs:
        s += __get_sh_python(args,infile)
    return s

def shpython_handler(args,parser):
    set_log_level(args)
    repls = get_sh_python(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_python_perl(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\n':
                s += '\\'
                s += '\\'
                s += 'n'
            elif c == '#':
                s += '\\'
                s += '\\'
                s += '#'
            elif c == '$':
                s += '\\' * 6
                s += '$'
            elif c == '"':
                s += '\\' * 6
                s += '"'
            elif c == '\\':
                s += '\\' * 8
            elif c == '\'':
                s += '\\'
                s += '\''
            elif c == '@':
                s += '\\' * 2
                s += '@'
            elif c == '`':
                s += '\\' * 2
                s += '`'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_python_perl(args):
    s = ''
    for infile in args.subnargs:
        s += __get_python_perl(args,infile)
    return s

def pythonperl_handler(args,parser):
    set_log_level(args)
    repls = get_python_perl(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def version_handler(args,parser):
    sys.stdout.write('insertcode VERSION_RELACE_STRING\n')
    sys.exit(0)
    return

def main():
    commandline='''
    {
        "verbose|v" : "+",
        "input|i##default (stdin)##" : null,
        "output|o##default (stdout)##": null,
        "pattern|p" : "%REPLACE_PATTERN%",
        "bashinsert<bashinsert_handler>" : {
            "$" : "*"
        },
        "bashstring<bashstring_handler>" : {
            "$" : "*"
        },
        "makepython<makepython_handler>" : {
            "$" : "*"
        },
        "makeperl<makeperl_handler>" : {
            "$" : "*"
        },
        "shperl<shperl_handler>" : {
            "$" : "*"
        },
        "shpython<shpython_handler>" : {
            "$" : "*"
        },
        "pythonperl<pythonperl_handler>" : {
            "$" : "*"
        },
        "version<version_handler>" : {
            "$" : 0
        }
    }
    '''
    options = extargsparse.ExtArgsOptions('{ "version" : "VERSION_RELACE_STRING"}')
    parser = extargsparse.ExtArgsParse()
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line(None,parser)
    sys.stderr.write('no handler specified')
    sys.exit(4)
    return

##importdebugstart
import disttools
import unittest
import tempfile
import subprocess
import cmdpack

class _LoggerObject(object):
    def __init__(self,cmdname='extargsparse'):
        self.__logger = logging.getLogger(cmdname)
        if len(self.__logger.handlers) == 0:
            loglvl = logging.WARN
            lvlname = '%s_LOGLEVEL'%(cmdname)
            lvlname = lvlname.upper()
            if lvlname in os.environ.keys():
                v = os.environ[lvlname]
                vint = 0
                try:
                    vint = int(v)
                except:
                    vint = 0
                if vint >= 4:
                    loglvl = logging.DEBUG
                elif vint >= 3:
                    loglvl = logging.INFO
            handler = logging.StreamHandler()
            fmt = "%(levelname)-8s %(message)s"
            fmtname = '%s_LOGFMT'%(cmdname)
            fmtname = fmtname.upper()
            if fmtname in os.environ.keys():
                v = os.environ[fmtname]
                if v is not None and len(v) > 0:
                    fmt = v
            formatter = logging.Formatter(fmt)
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)
            self.__logger.setLevel(loglvl)
            # we do not want any more output debug
            self.__logger.propagate = False

    def format_string(self,arr):
        s = ''
        if isinstance(arr,list):
            i = 0
            for c in arr:
                s += '[%d]%s\n'%(i,c)
                i += 1
        elif isinstance(arr,dict):
            for c in arr.keys():
                s += '%s=%s\n'%(c,arr[c])
        else:
            s += '%s'%(arr)
        return s

    def format_call_msg(self,msg,callstack):
        inmsg = ''  
        if callstack is not None:
            try:
                frame = sys._getframe(callstack)
                inmsg += '[%-10s:%-20s:%-5s] '%(frame.f_code.co_filename,frame.f_code.co_name,frame.f_lineno)
            except:
                inmsg = ''
        inmsg += msg
        return inmsg

    def info(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.info('%s'%(inmsg))

    def error(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.error('%s'%(inmsg))

    def warn(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.warn('%s'%(inmsg))

    def debug(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.debug('%s'%(inmsg))

    def fatal(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.fatal('%s'%(inmsg))

    def call_func(self,funcname,*args,**kwargs):
        mname = '__main__'
        fname = funcname
        try:
            if '.' not in funcname:
                m = importlib.import_module(mname)
            else:
                sarr = re.split('\.',funcname)
                mname = '.'.join(sarr[:-1])
                fname = sarr[-1]
                m = importlib.import_module(mname)
        except ImportError as e:
            self.error('can not load %s'%(mname))
            return None

        for d in dir(m):
            if d == fname:
                val = getattr(m,d)
                if hasattr(val,'__call__'):
                    return val(*args,**kwargs)
        self.error('can not call %s'%(funcname))
        return None


class insertcode_test(unittest.TestCase):
    def setUp(self):
        keyname = '_%s__logger'%(self.__class__.__name__)
        if getattr(self,keyname,None) is None:
            self.__logger = _LoggerObject('insertcode')
        self.__tmp_files = []
        self.__tmp_descrs = []
        return

    def info(self,msg,callstack=1):
        return self.__logger.info(msg,(callstack + 1))

    def error(self,msg,callstack=1):
        return self.__logger.error(msg,(callstack + 1))

    def warn(self,msg,callstack=1):
        return self.__logger.warn(msg,(callstack + 1))

    def debug(self,msg,callstack=1):
        return self.__logger.debug(msg,(callstack + 1))

    def fatal(self,msg,callstack=1):
        return self.__logger.fatal(msg,(callstack + 1))

    def __remove_file_ok(self,filename,description=''):
        ok = True
        if 'INSERTCODE_TEST_RESERVED' in os.environ.keys():
            ok = False
        if filename is not None and ok:
            os.remove(filename)
        elif filename is not None:
            self.error('%s %s'%(description,filename))
        return

    def tearDown(self):
        if len(self.__tmp_files) > 0:
            idx = 0
            assert(len(self.__tmp_descrs) == len(self.__tmp_files))
            while idx < len(self.__tmp_files):
                c = self.__tmp_files[idx]
                d = self.__tmp_descrs[idx]
                self.__remove_file_ok(c,d)
                idx += 1                
        self.__tmp_files = []
        self.__tmp_descrs = []
        return

    @classmethod
    def setUpClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def __write_temp_file(self,content,description='',suffix_add=None):
        if suffix_add is None:
            if sys.platform == 'win32':
                suffix_add = '.cpp'
            else:
                suffix_add = '.c'
        fd , tempf = tempfile.mkstemp(suffix=suffix_add,prefix='parse',dir=None,text=True)
        os.close(fd)
        with open(tempf,'w') as f:
            f.write('%s'%(content))
        self.info('tempf %s'%(tempf))
        self.__tmp_files.append(tempf)
        self.__tmp_descrs.append(description)
        return tempf        


    def test_A001(self):
        if sys.platform == 'win32':
            return
        topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
        echofile = os.path.join(topdir,'test','template','echocode.tmpl')
        infile = os.path.join(topdir,'test','bash','a.sh')
        cmds = '%s %s -i %s bashstring -p \'%%REPLACE_PATTERN%%\' %s | bash | diff -B - %s'%(sys.executable, __file__,echofile, infile,infile)
        self.info('cmds [%s]'%(cmds))
        subprocess.check_call(['bash','-c',cmds])
        return

    def test_A002(self):
        if sys.platform == 'win32':
            return
        topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
        echofile = os.path.join(topdir,'test','template','echocode_perl.mak.tmpl')
        infile = os.path.join(topdir,'test','perl','a.pl')
        cmds = '%s %s -i %s makeperl -p \'%%REPLACE_PATTERN%%\' %s | make  -f /dev/stdin | diff - %s'%(sys.executable, __file__,echofile, infile,infile)
        self.info('cmds [%s]'%(cmds))
        subprocess.check_call(['bash','-c',cmds])
        return

    def test_A003(self):
        if sys.platform == 'win32':
            return
        topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
        echofile = os.path.join(topdir,'test','template','echocode_python.mak.tmpl')
        infile = os.path.join(topdir,'test','python','a.py')
        cmds = '%s %s -i %s makepython -p \'%%REPLACE_PATTERN%%\' %s | make  -f /dev/stdin | diff - %s'%(sys.executable, __file__,echofile, infile,infile)
        self.info('cmds [%s]'%(cmds))
        subprocess.check_call(['bash','-c',cmds])
        return

    def test_A004(self):
        if sys.platform == 'win32':
            return
        topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
        echofile = os.path.join(topdir,'test','template','echocode_perl.sh.tmpl')
        infile = os.path.join(topdir,'test','perl','a.pl')
        cmds = '%s %s -i %s shperl -p \'%%REPLACE_PATTERN%%\' %s | bash | diff -B - %s'%(sys.executable, __file__,echofile, infile,infile)
        self.info('cmds [%s]'%(cmds))
        subprocess.check_call(['bash','-c',cmds])
        return

    def test_A005(self):
        if sys.platform == 'win32':
            return
        topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
        echofile = os.path.join(topdir,'test','template','echocode_python.sh.tmpl')
        infile = os.path.join(topdir,'test','python','a.py')
        cmds = '%s %s -i %s shpython -p \'%%REPLACE_PATTERN%%\' %s | bash | diff -B - %s'%(sys.executable, __file__,echofile, infile,infile)
        self.info('cmds [%s]'%(cmds))
        subprocess.check_call(['bash','-c',cmds])
        return


def debug_release():
    if '-v' in sys.argv[1:]:
        loglvl =  logging.DEBUG
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    tofile= os.path.abspath(os.path.join(topdir,'insertcode','__main__.py'))
    if len(sys.argv) > 2:
        for k in sys.argv[1:]:
            if not k.startswith('-'):
                tofile = k
                break
    versionfile = os.path.abspath(os.path.join(topdir,'VERSION'))
    if not os.path.exists(versionfile):
        raise Exception('can not find VERSION file')
    with open(versionfile,'r') as f:
        for l in f:
            l = l.rstrip('\r\n')
            vernum = l
            break
    sarr = re.split('\.',vernum)
    if len(sarr) != 3:
        raise Exception('version (%s) not format x.x.x'%(vernum))
    VERSIONNUMBER = vernum
    repls = dict()
    repls[r'VERSION_RELACE_STRING'] = VERSIONNUMBER
    repls[r'debug_main'] = 'main'
    #logging.info('repls %s'%(repls.keys()))
    disttools.release_file('__main__',tofile,[],[[r'##importdebugstart.*',r'##importdebugend.*']],[],repls)
    return

def test_main():
    sys.argv[1:] = sys.argv[2:]
    unittest.main()
    return

def debug_main():
    if '--release' in sys.argv[1:]:
        debug_release()
        return
    if len(sys.argv) > 1 and 'test' == sys.argv[1]:
        test_main()
        return
    main()
    return

##importdebugend

if __name__ == '__main__':
    debug_main()