from core.Controller import Controller

# 控制台
class index(Controller):

  # 首页
  def Index(self):
    return self.GetJSON({'code':0, 'msg':'Python Admin'})