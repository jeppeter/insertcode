#! /bin/bash

_script_file=`readlink -f $0`
script_dir=`dirname $_script_file`

rm -rf $script_dir/dist

rm -f $script_dir/insertcode/__main__.py.touched 
rm -f $script_dir/insertcode/__init__.py.touched

rm -f $script_dir/insertcode/__main__.py
rm -f $script_dir/insertcode/__init__.py

rm -f $script_dir/src/insertcode/__main_debug__.pyc
rm -f $script_dir/src/insertcode/__init_debug__.pyc

rm -f $script_dir/setup.py

rm -rf $script_dir/insertcode
rm -rf $script_dir/__pycache__
rm -rf $script_dir/src/insertcode/__pycache__
rm -rf $script_dir/insertcode.egg-info
