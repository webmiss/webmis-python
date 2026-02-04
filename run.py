#!/bin/python
# -*- coding: UTF-8 -*-
from core.Server import WSGIApplication
from wsgiref.simple_server import make_server, WSGIRequestHandler
from app.config.Env import Env

# 日志
class SilentRequestHandler(WSGIRequestHandler):
  def log_request(self, code='-', size='-'):
    # 屏蔽2开头
    code_str = str(code)
    if code_str.startswith('2'): return
    super().log_request(code, size)

# 实例化
app = WSGIApplication()
if __name__ == '__main__':
  # 开发
  print('[ Server ]', f"http://{Env.server_host}:{Env.server_port}")
  if(Env.mode=='dev'):
    server = make_server(Env.server_host, Env.server_port, app)
  else:
    server = make_server(Env.server_host, Env.server_port, app, handler_class=SilentRequestHandler)
  # 运行
  server.serve_forever()
