from core.Controller import Controller

# 消息
class Msg(Controller):

  # 列表
  def List(self):
    # 数据
    num: int = 0
    list: list = []
    # 返回
    return self.GetJSON({'code':0, 'data':{'num':num, 'list':list}})