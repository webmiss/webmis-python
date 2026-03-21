from core.Controller import Controller
from app.service.TokenAdmin import TokenAdmin

from app.models.ErpBasePartner import ErpBasePartner

# 控制台
class Index(Controller):

  __partner: dict = {}     # 主仓

  # 首页
  def Index(self):
    return self.GetJSON({'code':0, 'msg':'Python Admin'})
  
  # 软件升级
  def Version(self):
    # 参数
    json = self.Json()
    os: str = self.JsonName(json, 'os')
    local = self.JsonName(json, 'version')
    # 验证
    os = os.lower()
    if os not in ['web']: return self.GetJSON({'code':4000, 'msg':'['+os+']该操作系统不支持更新!'})
    # 数据
    size = 0
    version = url = ''
    if os == 'web':
      version = '3.0.0'
      url = 'https://admin.webmis.vip'
      size = 0
    return self.GetJSON({'code':0, 'data':{'os':os, 'version':version, 'local':local, 'size':size, 'url':url}})
  
  # 法定假期
  def Holiday(self):
    # 参数
    json = self.Json()
    date: str = self.JsonName(json, 'date')
    url: str = 'https://python.webmis.vip/upload/img/holiday/'
    # 假期
    holiday = {
      '2026-02-16': {'holiday':True, 'name':'春节', 'img':url+'20260216(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-17': {'holiday':True, 'name':'春节', 'img':url+'20260217(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-18': {'holiday':True, 'name':'春节', 'img':url+'20260218(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-19': {'holiday':True, 'name':'春节', 'img':url+'20260219(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-20': {'holiday':True, 'name':'春节', 'img':url+'20260220(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-21': {'holiday':True, 'name':'春节', 'img':url+'20260221(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-22': {'holiday':True, 'name':'春节', 'img':url+'20260222(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-23': {'holiday':True, 'name':'春节', 'img':url+'20260223(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-04-04': {'holiday':True, 'name':'清明节', 'img':'', 'bg':''},
      '2026-04-05': {'holiday':True, 'name':'清明节', 'img':'', 'bg':''},
      '2026-04-06': {'holiday':True, 'name':'清明节', 'img':'', 'bg':''},
      '2026-05-01': {'holiday':True, 'name':'劳动节', 'img':'', 'bg':''},
      '2026-05-02': {'holiday':True, 'name':'劳动节', 'img':'', 'bg':''},
      '2026-05-03': {'holiday':True, 'name':'劳动节', 'img':'', 'bg':''},
      '2026-05-04': {'holiday':True, 'name':'劳动节', 'img':'', 'bg':''},
      '2026-05-05': {'holiday':True, 'name':'劳动节', 'img':'', 'bg':''},
      '2026-06-20': {'holiday':True, 'name':'端午节', 'img':'', 'bg':''},
      '2026-06-21': {'holiday':True, 'name':'端午节', 'img':'', 'bg':''},
      '2026-06-22': {'holiday':True, 'name':'端午节', 'img':'', 'bg':''},
      '2026-09-26': {'holiday':True, 'name':'中秋节', 'img':'', 'bg':''},
      '2026-09-27': {'holiday':True, 'name':'中秋节', 'img':'', 'bg':''},
      '2026-09-28': {'holiday':True, 'name':'中秋节', 'img':'', 'bg':''},
      '2026-10-01': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
      '2026-10-02': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
      '2026-10-03': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
      '2026-10-04': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
      '2026-10-05': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
      '2026-10-06': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
      '2026-10-07': {'holiday':True, 'name':'国庆节', 'img':'', 'bg':''},
    }
    # 返回
    return self.GetJSON({'code':0, 'data': holiday[date] if date in holiday else '' })
  
  # 选项
  def GetSelect(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    # 验证
    msg = TokenAdmin().Verify(token, '')
    if msg != '' : return self.GetJSON({'code':4001})
    # 仓库
    self.__partner = ErpBasePartner().GetList(['type=0', 'status=1'])
    partner_name = []
    for k,v in self.__partner.items():
      partner_name.append({'label': v['name'], 'value': k})
    # 返回
    return self.GetJSON({'code':0, 'data':{
      'partner': partner_name
    }})
