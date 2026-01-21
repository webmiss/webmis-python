from core.Controller import Controller

# 网站
class index(Controller):

  # 首页
  def index(self):
    return self.GetJSON({'code':0, 'msg':'Python Web'})