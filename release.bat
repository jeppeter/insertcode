echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF
echo %script_dir%

if -%PYTHON%- == -- (
	set PYTHON=python
)

echo "PYTHON [%PYTHON%]"

%PYTHON% %script_dir%src\insertcode\__main_debug__.py test -f
if not errorlevel 0 (
	echo "not test ok" >&2
	goto :fail
)

del /Q /F %script_dir%insertcode\__main__.py.touched 2>NUL
del /Q /F %script_dir%insertcode\__init__.py.touched 2>NUL

%PYTHON% %script_dir%make_setup.py

%PYTHON% %script_dir%src\insertcode\__init_debug__.py --release -v %script_dir%insertcode\__init__.py
call :check_file %script_dir%insertcode\__init__.py.touched

%PYTHON% %script_dir%src\insertcode\__main_debug__.py --release -v %script_dir%insertcode\__main__.py
call :check_file %script_dir%insertcode\__main__.py.touched



goto :end

:check_file

set _waitf=%1
set _maxtime=100
set _cnt=0
set _checked=0
if x%_waitf% == x (
	goto :check_file_end
)

:check_file_again
if %_maxtime% LSS %_cnt% (
	echo "can not wait (%_waitf%) in (%_maxtime%)"
	exit /b 3
)

if exist %_waitf% (
	%PYTHON% -c "import time;time.sleep(0.1)"
	set /A _checked=%_checked%+1
	if %_checked% GTR 3 (
		del /F /Q %_waitf%
		goto :check_file_end
	)
    echo "will check (%_checked%) %_waitf%"
) else (
	set _checked=0
)

set /A _cnt=%_cnt%+1
%PYTHON% -c "import time;time.sleep(0.1)"
goto :check_file_again

:check_file_end
exit /b 0

:makesuredel
if not exist %1 (
	echo "not exist %1"
	exit /b 3
)

del /F /Q %1
exit /b 0

:fail

goto :last
:end


copy /Y %script_dir%README.md %script_dir%insertcode\README

:last
echo on