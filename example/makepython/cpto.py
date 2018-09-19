#! /usr/bin/env python

import sys
import shutil

def main():
	if len(sys.argv[1:]) >= 2:
		shutil.copy2(sys.argv[1],sys.argv[2])
	return

main()