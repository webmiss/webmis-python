from core.Controller import Controller
from core.Redis import Redis
from app.config.Env import Env
from app.service.TokenAdmin import TokenAdmin
from app.librarys.Safety import Safety
from app.util.Util import Util
from app.util.Time import Time
from app.util.Hash import Hash

from app.models.User import User as UserM

# 用户
class User(Controller):

  # 登录
  def Login(self):
    # 参数
    json = self.Json()
    uname: str = self.JsonName(json, 'uname')
    passwd = self.JsonName(json, 'passwd')
    vcode = self.JsonName(json, 'vcode')
    vcode_url = self.BaseUrl('admin/user/vcode')+'/'+uname+'?'+str(Time.Time())
    # 验证
    if not Safety.IsRight('uname', uname) and not Safety.IsRight('tel', uname) and not Safety.IsRight('email', uname):
      return self.GetJSON({'code':4000, 'msg':self.GetLang('login_uname')})
    if not passwd and not vcode:
      return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify')})
    # 登录方式
    where: str = ''
    vcode: str = Util.Trim(vcode).lower()
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
      where = '(a.uname="'+uname+'" OR a.tel="'+uname+'" OR a.email="'+uname+'") AND a.password="'+Hash.Md5(passwd)+'"'
    else:
      # 验证码
      redis = Redis()
      code = redis.Get(Env.admin_token_prefix+'_vcode_'+uname)
      if not code or code != vcode : return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify_vcode')})
      # 条件
      where = 'a.tel="'+uname+'"'
    # 查询
    m = UserM()
    m.Table('user a')
    m.LeftJoin('user_info AS b', 'a.id=b.uid')
    m.LeftJoin('sys_perm AS c', 'a.id=c.uid')
    m.LeftJoin('sys_role AS d', 'c.role=d.id')
    m.Columns(
      'a.id', 'a.status', 'a.password', 'a.tel', 'a.email',
      'b.type', 'b.nickname', 'b.department', 'b.position', 'b.name', 'b.gender', 'FROM_UNIXTIME(b.birthday, "%%Y-%%m-%%d") as birthday', 'b.img', 'b.signature',
      'c.role', 'c.perm', 'c.brand', 'c.shop', 'c.partner', 'c.partner_in', 
      'd.perm as role_perm'
    )
    m.Where(where)
    data = m.FindFirst()
    # 是否存在
    if not data :
      # 强制验证码(24小时)
      redis = Redis()
      redis.Set(Env.admin_token_prefix+'_vcode_'+uname, Time.Time())
      redis.Expire(Env.admin_token_prefix+'_vcode_'+uname, 24*3600)
      # 返回
      return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify'), 'vcode_url':vcode_url})
    else :
      # 清除验证码
      redis = Redis()
      redis.Del(Env.admin_token_prefix+'_vcode_'+uname)
    # 是否禁用
    if int(data['status']) == 0 : return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify_status')})
    # 默认密码
    isPasswd: bool = data['password'] == Hash.Md5(Env.password)
    # 权限
    perm: str = data['role_perm']
    if data['perm'] : perm = data['perm']
    if not perm : return self.GetJSON({'code':4000, 'msg':self.GetLang('login_verify_perm')})
    TokenAdmin().SavePerm(str(data['id']), perm)
    self.Print(data, perm)
    # 返回
    return self.GetJSON({'code':0, 'data':{}})