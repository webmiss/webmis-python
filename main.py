#!/bin/python
# -*- coding: UTF-8 -*-
from core.Server import WSGIServer

if __name__ == '__main__':
  server = WSGIServer()
  server.run(host='127.0.0.1', port=9010)