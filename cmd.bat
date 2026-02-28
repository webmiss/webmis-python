@echo off
CHCP 65001 >nul 2>&1

REM 配置
set s=%1%
set dev=run_dev.py
set cli=cli.py
set python_url=https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe
set package=watchdog pymysql redis pyjwt

@REM 临时环境变量
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SysPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"
set "PATH=%SysPath%;%UserPath%"
@REM Python环境
python --version >nul 2>&1
if %errorLevel% neq 0 (
  @REM 下载文件
  echo [✓] 下载文件: %python_url%
  curl -L "%python_url%" -o python.exe
  @REM 安装
  echo [✓] 正在安装: python.exe
  python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
  @REM 清除文件
  del python.exe >nul 2>&1
  echo [✓] 安装成功: 正在刷新环境变量
  @REM 验证
  python --version >nul 2>&1
  if %errorLevel% neq 0 (
    @REM 临时环境变量
    for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SysPath=%%b"
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"
    set "PATH=%SysPath%;%UserPath%"
    @REM 查看版本
    python --version
    pip --version
  )
)

REM 运行
 if "%s%"=="serve" (
  python %dev%
REM 安装
) else if "%s%"=="install" (
  pip install %package%
  echo [✓] 运行: .\cmd serve
REM Socket-运行
) else if "%s%"=="socket" (
  ( python %cli% socket start ) || ( echo ^> 请安装'python' )
) else (
  echo ----------------------------------------------------
  echo [use] cmd.bat ^<command^>
  echo ----------------------------------------------------
  echo ^<command^>
  echo   serve         运行: python %dev%
  echo   install       依赖包: pip install %package%
  echo ^<Socket^>
  echo   socket        运行
  echo ----------------------------------------------------
)