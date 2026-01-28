from core.Controller import Controller
from flask import request

# 接口
class Index(Controller):

  # 首页
  def Index(self):
    return self.GetJSON({'code':0, 'msg':'Python Api'})