from core.Model import Model

# 角色
class SysRole(Model):

  # 构造函数
  def __init__(self):
    self.DBConfig('default')
    self.Table('sys_role')