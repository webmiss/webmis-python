from core.Controller import Controller

from app.models.User import User

# 接口
class Index(Controller):

  # 首页
  def Index(self):
    m = User()
    m.Values({'uname':'admin1', 'upwd':'123456'})
    data = m.Insert()
    # m.Columns('id', 'uname')
    # m.Where('uname=%s', 'admin1')
    # data = m.Find()
    self.Print(data, m.GetNums())
    return self.GetJSON({'code':0, 'msg':'Python Api'})