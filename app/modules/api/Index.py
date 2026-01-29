from core.Controller import Controller

from app.models.User import User

# 接口
class Index(Controller):

  # 首页
  def Index(self):
    m = User()
    return self.GetJSON({'code':0, 'msg':'Python Api'})