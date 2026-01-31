from core.Controller import Controller

from app.models.User import User

# 接口
class Index(Controller):

  # 首页
  def Index(self):
    # 查询
    m = User()
    m.Columns('id', 'uname')
    data = m.Find()
    sql = m.GetSql()
    self.Print(data, sql, m.GetNums())
    # 返回
    return self.GetJSON({'code':0, 'msg':'Python Api'})