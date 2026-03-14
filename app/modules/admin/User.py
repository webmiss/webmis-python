from core.Controller import Controller
from app.util.Time import Time

# 用户
class User(Controller):

  # 登录
  def Login(self):
    # 参数
    json = self.Json()
    uname: str = self.JsonName(json, 'uname')
    passwd = self.JsonName(json, 'passwd')
    vcode = self.JsonName(json, 'vcode')
    vcode_url = self.BaseUrl('admin/user/vcode')+'/'+uname+'?'+str(Time.time())
    self.Print(uname, passwd, vcode, vcode_url)
    return self.GetJSON({'code':0, 'data':{}})