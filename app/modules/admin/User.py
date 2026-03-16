from core.Controller import Controller
from core.Redis import Redis
from app.config.Env import Env
from app.util.Util import Util
from app.util.Time import Time
from app.util.Hash import Hash
from app.librarys.Safety import Safety

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
    # 验证
    if not Safety.IsRight('uname', uname) and not Safety.IsRight('tel', uname) and not Safety.IsRight('email', uname):
      return self.GetJSON({'code':4000, 'msg':self.GetLang('login_uname')})
    if not passwd and not vcode:
      return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify')})
    # 登录方式
    where: str = ''
    vcode: str = Util.trim(vcode).lower()
    if passwd :
      # 密码长度
      if not Safety.IsRight('passwd', passwd):
        return self.GetJSON({'code':4000, 'msg':self.GetLang('login_passwd', 6, 16)})
      # 验证码
      redis = Redis()
      code = redis.Get(Env.admin_token_prefix+'_vcode_'+uname)
      if code :
        if len(vcode)!=4 : return self.GetJSON({'code':4001, 'msg':self.GetLang('login_vcode'), 'vcode_url':vcode_url})
        elif code != vcode : return self.GetJSON({'code':4002, 'msg':self.GetLang('login_verify_vcode'), 'vcode_url':vcode_url})
      # 条件
      where = '(a.uname="'+uname+'" OR a.tel="'+uname+'" OR a.email="'+uname+'") AND a.password="'+Hash.md5(passwd)+'"'
      self.Print('redis', code, where)
    else:
      # 验证码
      redis = Redis()
      code = redis.Get(Env.admin_token_prefix+'_vcode_'+uname)
      if not code or code != vcode : return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify_vcode')})
      # 条件
      where = 'a.tel="'+uname+'"'
    self.Print(uname, passwd, vcode, where)
    # 返回
    return self.GetJSON({'code':0, 'data':{}})