from core.Controller import Controller
from app.service.TokenAdmin import TokenAdmin
from app.config.Env import Env
from app.librarys.FileEo import FileEo
from app.librarys.Upload import Upload
from app.util.Util import Util
from app.util.Time import Time

# 系统用户
class SysUser(Controller):

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
    # 数据
    list = []
    # 返回
    return self.GetJSON({'code':0, 'time':Time.Date('Y-m-d H:i:s'), 'data': list})

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
    self.Print(where)
    # 数据
    list = []
    # 返回
    return self.GetJSON({'code':0, 'time':Time.Date('Y-m-d H:i:s'), 'data': list})
  
  # 搜索条件
  def __getWhere(self, d: dict) -> str:
    where = []
    # 时间
    stime = d['stime'] if d.get('stime') else Time.Date('Y-m-d')
    start = Time.StrToTime(stime+' 00:00:00')
    where.append('a.ltime>='+str(start))
    # 结果
    return Util.Implode(' AND ', where)
