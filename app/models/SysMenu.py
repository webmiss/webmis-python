from core.Model import Model

# 系统菜单
class SysMenu(Model):

  # 构造函数
  def __init__(self):
    self.DBConn('default')
    self.Table('sys_menus')