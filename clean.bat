
echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF

rmdir /Q /S %script_dir%dist 2>NUL

del /Q /F %script_dir%insertcode\__main__.py.touched 2>NUL
del /Q /F %script_dir%insertcode\__init__.py.touched 2>NUL

del /Q /F %script_dir%insertcode\__main__.py 2>NUL
del /Q /F %script_dir%insertcode\__init__.py 2>NUL

del /Q /F %script_dir%src\insertcode\__main_debug__.pyc 2>NUL
del /Q /F %script_dir%src\insertcode\__init_debug__.pyc 2>NUL

del /Q /F %script_dir%setup.py 2>NUL


rmdir /Q /S %script_dir%insertcode 2>NUL
rmdir /Q /S %script_dir%__pycache__ 2>NUL
rmdir /Q /S %script_dir%src\insertcode\__pycache__ 2>NUL
rmdir /Q /S %script_dir%insertcode.egg-info 2>NUL
rmdir /Q /S %script_dir%build 2>NUL
