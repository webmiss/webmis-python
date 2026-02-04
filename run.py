#!/bin/python
# -*- coding: UTF-8 -*-
from core.Server import WSGIApplication
from wsgiref.simple_server import make_server, WSGIRequestHandler
from app.config.Env import Env

# 屏蔽日志
class SilentRequestHandler(WSGIRequestHandler):
  def log_request(self, code='-', size='-'): pass

# 实例化
app = WSGIApplication()
if __name__ == '__main__':
  # 开发
  if(Env.mode=='dev'):
    server = make_server(Env.server_host, Env.server_port, app)
  else:
    server = make_server(Env.server_host, Env.server_port, app, handler_class=SilentRequestHandler)
  # 运行
  print('[ Server ]', f"http://{Env.server_host}:{Env.server_port}")
  server.serve_forever()
