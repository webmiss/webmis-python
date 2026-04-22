from core.Controller import Controller
from app.service.TokenAdmin import TokenAdmin
from app.service.Status import Status
from app.service.Data import Data
from app.config.Env import Env
from app.librarys.FileEo import FileEo
from app.librarys.Upload import Upload
from app.util.Util import Util
from app.util.Time import Time

from app.models.User import User
from app.models.SysRole import SysRole

# 系统用户
class SysUser(Controller):

  __type_name: dict = {}    # 类型
  __status_name: dict = {}  # 状态

  # 统计
  def Total(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    data: str = self.JsonName(json, 'data')
    # 验证
    msg = TokenAdmin().Verify(token, '')
    if msg != '' : return self.GetJSON({'code':4001})
    if not data : return self.GetJSON({'code':4000})
    # 条件
    where = self.__getWhere(data)
    # 统计
    m = User()
    m.Table('user as a')
    m.LeftJoin('user_info as b', 'a.id=b.uid')
    m.LeftJoin('sys_perm as c', 'a.id=c.uid')
    m.LeftJoin('sys_role as d', 'c.role=d.id')
    m.Columns('count(*) AS total')
    m.Where(where)
    one = m.FindFirst()
    # 数据
    total = {'total':0}
    if one : total['total'] = int(one['total'])
    # 返回
    return self.GetJSON({'code':0, 'time':Time.Date('Y-m-d H:i:s'), 'data': total})

  # 列表
  def List(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    data: dict = self.JsonName(json, 'data')
    page: int = self.JsonName(json, 'page')
    limit: int = self.JsonName(json, 'limit')
    order: str = self.JsonName(json, 'order')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not data or not page or not limit : return self.GetJSON({'code':4000})
    # 条件
    where = self.__getWhere(data)
    # 查询
    m = User()
    m.Table('user as a')
    m.LeftJoin('user_info as b', 'a.id=b.uid')
    m.LeftJoin('sys_perm as c', 'a.id=c.uid')
    m.LeftJoin('sys_role as d', 'c.role=d.id')
    m.Columns(
      'a.id', 'a.uname', 'a.email', 'a.tel', 'a.status', 'FROM_UNIXTIME(a.rtime, "%%Y-%%m-%%d %%H:%%i:%%s") as rtime', 'FROM_UNIXTIME(a.ltime, "%%Y-%%m-%%d %%H:%%i:%%s") as ltime', 'FROM_UNIXTIME(a.utime, "%%Y-%%m-%%d %%H:%%i:%%s") as utime',
      'b.type', 'b.nickname', 'b.department', 'b.position', 'b.name', 'b.gender', 'b.img', 'b.remark', 'FROM_UNIXTIME(b.birthday, "%%Y-%%m-%%d") as birthday',
      'c.role', 'c.perm',
      'd.name as role_name',
    )
    m.Where(where)
    m.Order(order if order else 'a.ltime DESC')
    m.Page(page, limit)
    list = m.Find()
    # 数据
    self.__type_name = Status.Public('role_name')
    for v in list:
      v['status'] = True if v['status']==1 else False
      v['type_name'] = self.__type_name[v['type']] if v['type'] in self.__type_name.keys() else '-'
      v['role_name'] = v['role_name'] if v['role_name']!=None else ('私有' if not v['perm'] else '-')
      v['img'] = Data().Img(v['img'])
    # 返回
    return self.GetJSON({'code':0, 'time':Time.Date('Y-m-d H:i:s'), 'data': list})
  
  # 搜索条件
  def __getWhere(self, d: dict) -> str:
    where = []
    # 时间
    stime = d['stime'] if d.get('stime') else Time.Date('Y-m-d')
    start = Time.StrToTime(stime+' 00:00:00')
    where.append('a.ltime>='+str(start))
    etime = d['etime'] if d.get('etime') else Time.Date('Y-m-d')
    end = Time.StrToTime(etime+' 23:59:59')
    where.append('a.ltime<='+str(end))
    # 结果
    return Util.Implode(' AND ', where)

  # 选项
  def GetSelect(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    # 验证
    msg = TokenAdmin().Verify(token, '')
    if msg != '' : return self.GetJSON({'code':4001})
    # 类型
    type_name = []
    self.__type_name = Status.Public('role_name')
    for k, v in self.__type_name.items():
      type_name.append({'label':v, 'value':k})
    # 角色
    m = SysRole()
    m.Columns('id', 'name')
    m.Where('status=1')
    all = m.Find()
    role_name = [{'label':'无', 'value':''}]
    for v in all:
      role_name.append({'label':v['name'], 'value':v['id']})
    # 状态
    status_name = []
    self.__status_name = Status.Public('status_name')
    for k, v in self.__status_name.items():
      status_name.append({'label':v, 'value':k})
    # 返回
    return self.GetJSON({'code':0, 'data': {
      'type_name': type_name,
      'role_name': role_name,
      'status_name': status_name
    }})
