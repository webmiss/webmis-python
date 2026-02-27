@echo off
CHCP 65001 >nul 2>&1

REM 配置
set s=%1%
set dev=run_dev.py
set cli=cli.py
set python_url=https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe
set package=watchdog pymysql redis pyjwt

@REM Python环境
python --version >nul 2>&1
if %errorLevel% neq 0 (
  @REM 下载文件
  echo [✓] 下载文件：%python_url%
  curl -L "%python_url%" -o python.exe
  @REM 安装
  python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
  @REM 清除文件
  del python.exe >nul 2>&1
  echo [✓] 安装成功：正在刷新环境变量或重启终端
)
@REM 环境变量
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SysPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"
set "PATH=%SysPath%;%UserPath%"
@REM 查看版本
python --version && pip --version
if %errorLevel% neq 0 (
  echo [✗] 请手动下载安装: %python_url%
  exit /b 1
)

REM 运行
 if "%s%"=="serve" (
  python %dev%
REM 安装
) else if "%s%"=="install" (
  pip install %package%
REM Socket-运行
) else if "%s%"=="socket" (
  ( python %cli% socket start ) || ( echo ^> 请安装'python' )
) else (
  echo ----------------------------------------------------
  echo [use] cmd.bat ^<command^>
  echo ----------------------------------------------------
  echo ^<command^>
  echo   serve         运行: php -S %ip%:%port% -t public
  echo   install       依赖包: composer install
  echo ^<Socket^>
  echo   socket        运行
  echo ----------------------------------------------------
)