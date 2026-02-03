from core.Controller import Controller
from core.Redis import Redis

from app.models.User import User

# 接口
class Index(Controller):

  # 首页
  def Index(self):
    # 查询
    m = User()
    m.Columns('id', 'uname')
    data = m.Find()
    # Redis
    r = Redis()
    r.Set('test', 'Python Redis')
    self.Print(data, r.Get('test'))
    # 返回
    return self.GetJSON({'code':0, 'msg':'Python Api'})