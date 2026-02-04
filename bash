#!/bin/bash

# 配置
s=$1
index="run_dev.py"
config="uwsgi/uwsgi.ini"
pid="uwsgi/uwsgi.pid"
cli="cli.py"
package="watchdog pymysql redis pyjwt"
# package="python-dateutil flask flask_cors PyJWT redis wheel DBUtils pymysql websockets websocket-client qrcode Image zxing oss2"

# 运行
if [ "$s" == "serve" ]; then
  python $index
# 安装
elif [ "$s" == "install" ]; then
  {
    sudo pip install $package
  } || {
    pip install $package
  } || {
    echo "> 请安装'pip'"
  }
# 启动
elif [ "$s" == "start" ]; then
  uwsgi --ini $config
# 停止
elif [ "$s" == "stop" ]; then
  uwsgi --ini $pid
# Socket-运行
elif [ "$s" == "socket" ]; then
  {
    python $cli socket start
  } || {
    echo "> 请安装'python'"
  }
# Socket-启动
elif [ "$s" == "socketStart" ]; then
  python $cli socket start &
# Socket-停止
elif [ "$s" == "socketStop" ]; then
  ps -aux | grep "$cli socket start" | grep -v grep | awk {'print $2'} | xargs kill
else
  echo "----------------------------------------------------"
  echo "[use] ./bash <command>"
  echo "----------------------------------------------------"
  echo "<command>"
  echo "  serve         运行"
  echo "  install       安装依赖包: $package"
  echo "<Server>"
  echo "  start         启动: uwsgi --ini $config &"
  echo "  stop          停止"
  echo "<Socket>"
  echo "  socket        运行"
  echo "  socketStart   启动"
  echo "  socketStop    停止"
  echo "----------------------------------------------------"
fi

