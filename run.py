#!/bin/python
# -*- coding: UTF-8 -*-
from core.Server import WSGIApplication
from app.config.Env import Env

# 实例化
app = WSGIApplication()
if __name__ == '__main__':
  from wsgiref.simple_server import make_server
  # 开发
  if(Env.mode=='dev'):
    print('Local:', f"http://{Env.server_host}:{Env.server_port}")
  # 服务
  server = make_server(Env.server_host, Env.server_port, app)
  server.serve_forever()
