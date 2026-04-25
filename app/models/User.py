from core.Model import Model

# 用户表
class User(Model):

  # 构造函数
  def __init__(self):
    self.DBConfig('default')
    self.Table('user')