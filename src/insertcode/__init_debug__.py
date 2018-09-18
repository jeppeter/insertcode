#!/usr/bin/env python

##importdebugstart
import disttools
import logging
import re
import sys
import os

def debug_release():
    if '-v' in sys.argv[1:]:
        #sys.stderr.write('will make verbose\n')
        loglvl =  logging.DEBUG
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    tofile= os.path.abspath(os.path.join(topdir,'insertcode','__init__.py'))
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
    VERSIONINFO='( %s, %s, %s)'%(sarr[0],sarr[1],sarr[2])
    repls = dict()
    repls[r'VERSIONNUMBER'] = VERSIONNUMBER
    repls[r'"VERSIONINFO"'] = VERSIONINFO
    repls[r'__main_debug__'] = r'__main__'
    #logging.info('repls %s'%(repls.keys()))
    disttools.release_file('__main__',tofile,[r'^debug_*'],[[r'##importdebugstart.*',r'##importdebugend.*']],[],repls)
    return

def debug_main():
	if '--release' in sys.argv[1:]:
		debug_release()
		return
	return

if __name__ == '__main__':
	debug_main()
##importdebugend