from core.Controller import Controller
from app.service.TokenAdmin import TokenAdmin
from app.util.Util import Util

from app.models.SysMenu import SysMenu

# 系统菜单
class SysMenus(Controller):

  __menus: dict = {}          # 全部菜单
  __permAll: dict = {}        # 用户权限

  # 获取菜单-权限
  def GetMenusPerm(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    # 验证
    msg = TokenAdmin().Verify(token, '')
    if msg != '' : return self.GetJSON({'code':4001})
    # 用户权限
    self.__permAll = TokenAdmin().GetPerm(token)
    # 全部菜单
    self._getMenus()
    # 返回
    data = self._getMenusPerm('0')
    return self.GetJSON({'code':0, 'data':data})
  
  # 递归菜单
  def _getMenusPerm(self, fid: str):
    data = []
    M = self.__menus[fid] if fid in self.__menus else []
    for val in M :
      # 菜单权限
      id = str(val['id'])
      if id not in self.__permAll.keys() : continue
      # 动作权限
      perm = int(self.__permAll[id])
      action = []
      actionArr = []
      actionStr = str(val['action'])
      if actionStr != '' : actionArr = Util.JsonDecode(actionStr)
      for v in actionArr :
        permVal = int(v['perm'])
        if (perm&permVal)>0 : action += [v]
      # 数据
      value = {'url': val['url'], 'controller': val['controller'], 'action': action}
      langs = {'en_US': val['en_US'], 'zh_CN': val['zh_CN']}
      tmp = {'icon': val['ico'], 'label': val['title'], 'en': val['en'], 'value': value, 'langs':langs}
      menu = self._getMenusPerm(id)
      if len(menu)>0 : tmp['children']=menu
      data += [tmp]
    return data
  
  # 全部菜单
  def _getMenus(self):
    m = SysMenu()
    m.Columns(
      'id', 'fid', 'title', 'en', 'url', 'ico', 'controller', 'sort', 'status',
      'en_US', 'zh_CN',
      'FROM_UNIXTIME(ctime, "%%Y-%%m-%%d %%H:%%i:%%s") as ctime', 'FROM_UNIXTIME(utime, "%%Y-%%m-%%d %%H:%%i:%%s") as utime',
      'action', 'remark'
    )
    m.Order('sort, id')
    data = m.Find()
    # 数据
    self.__menus = {}
    for v in data:
      fid = str(v['fid'])
      if fid in self.__menus : self.__menus[fid] += [v]
      else : self.__menus[fid] = [v]