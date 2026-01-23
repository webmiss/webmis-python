#!/bin/python
# -*- coding: UTF-8 -*-
from core import application
from app.config.Env import Env

if __name__ == '__main__':
  from wsgiref.simple_server import make_server
  if(Env.mode=='dev'): print('Local:', f"http://{Env.server_host}:{Env.server_port}")
  server = make_server(Env.server_host, Env.server_port, application)
  server.serve_forever()
