from core.Base import Base
from core.Redis import Redis
from app.config.Env import Env
from app.util.Util import Util
from app.util.Time import Time
from app.util.Hash import Hash
from app.librarys.Safety import Safety

from app.models.SysMenu import SysMenu

# Token Admin
class TokenAdmin(Base):
    
  # 验证
  def Verify(self, token: str, urlPerm) -> str:
    # Token
    if token == '' : return 'Token不能为空!'
    tData = Safety.Decode(token)
    if tData == None : return 'Token验证失败!'
    # 是否过期
    uid = tData['uid']
    key = Env.admin_token_prefix+'_token_'+uid
    redis = Redis()
    time = redis.Ttl(key)
    if time < 1 : return '请重新登录!'
    # 单点登录
    access_token = redis.Get(key)
    if Env.admin_token_sso and Hash.Md5(token)!=access_token : return '强制退出!'
    # 是否续期
    if Env.admin_token_auto :
      redis.Expire(key, Env.admin_token_time)
      redis.Expire(Env.admin_token_prefix+'_perm_'+uid, Env.admin_token_time)
    # URL权限
    if urlPerm == '' : return ''
    arr = Util.Explode(urlPerm, '/')
    action = Util.Explode(arr[-1], '?')[0]
    arr.pop()
    controller = Util.Implode(arr, '/')
    # 查询菜单
    m = SysMenu()
    m.Columns('id', 'action')
    m.Where('controller=%s', controller)
    data = m.FindFirst()
    if data == None : return '菜单验证无效!'
    # 验证菜单
    id: str = data['id']
    perm: dict = self.GetPerm(token)
    if not perm[id] : return '无权访问菜单!'
    # 验证动作
    permVal: int = 0
    actionVal: int = int(perm[id])
    permArr = data['action'] 
    return ''
  
  # 权限-保存
  def SavePerm(self, uid: str, perm: str) -> bool:
    key = Env.admin_token_prefix+'_perm_'+uid
    redis = Redis()
    redis.Set(key, perm)
    redis.Expire(key, Env.admin_token_time)
    return True

  # 权限-获取
  def GetPerm(self, token: str) -> dict:
    arr = {}
    # Token
    if token == '' : return arr
    tData = Safety.Decode(token)
    if tData == None : return arr
    # 权限
    uid = str(tData['uid'])
    redis = Redis()
    permStr = redis.Get(Env.admin_token_prefix+'_perm_'+uid)
    if not permStr : return arr
    # 拆分
    perm = Util.Explode(permStr, ' ')
    for i in perm:
      tmp = Util.Explode(i, ':')
      arr[tmp[0]] = tmp[1] 
    return arr
  
  # 生成
  def Create(self, data: dict) -> str:
    # 登录时间
    data['l_time'] = Time.Date('%Y-%m-%d %H:%M:%S')
    token: str = Safety.Encode(data)
    # 缓存Token
    key: str = Env.admin_token_prefix+'_token_'+str(data['uid'])
    redis = Redis()
    redis.Set(key, Hash.Md5(token))
    redis.Expire(key, Env.admin_token_time)
    return token
  
  # 解析
  def Token(self, token: str) -> dict|None:
    tData = Safety.Decode(token)
    if tData == None : return None
    # 过期时间
    redis = Redis()
    tData['time'] = redis.Ttl(Env.admin_token_prefix+'_token_'+str(tData['uid']))
    return tData
