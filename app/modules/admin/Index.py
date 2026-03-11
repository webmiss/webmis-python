from core.Controller import Controller

# 控制台
class Index(Controller):

  # 首页
  def Index(self):
    return self.GetJSON({'code':0, 'msg':'Python Admin'})
  
  # 软件升级
  def Version(self):
    # 参数
    json = self.Json()
    os: str = self.JsonName(json, 'os')
    local = self.JsonName(json, 'version')
    # 数据
    os = os.lower()
    if os not in ['web']: return self.GetJSON({'code': 4000, 'msg': '['+os+']该操作系统不支持更新!'})
    version = size = url = ''
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
    url: str = 'https://php.webmis.vip/upload/img/holiday/'
    # 假期
    holiday = {
      '2026-02-16': {'holiday':True, 'name':'春节', 'img':url+'20260216(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-17': {'holiday':True, 'name':'春节', 'img':url+'20260217(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-18': {'holiday':True, 'name':'春节', 'img':url+'20260218(360x420).png', 'bg':url+'202602(360x50).png'},
      '2026-02-19': {'holiday':True, 'name':'春节', 'img':url+'20260219(360x420).png', 'bg':url+'202602(360x50).png'},
    }
    # 返回
    return self.GetJSON({'code':0, 'data': holiday[date] if date in holiday else '' })