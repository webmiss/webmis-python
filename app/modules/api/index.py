from core.Controller import Controller
from flask import request

# 接口
class index(Controller):

  # 首页
  def index(self):
    return self.GetJSON({'code':0, 'msg':'Python Api'})