import json, importlib, importlib.util
from core.Base import Base

# 控制器
class Controller(Base):

  get_raw: dict = {}    # Get参数
  post_raw: dict = {}   # Post参数

  # 获取语言
  def GetLang(self, action: str, *argv) -> str:
    lang: str = self.Get('lang')
    lang = lang.lower() if lang!=None and lang!='' else 'en_us'
    # 动态类
    module_name = f"app.config.langs.{lang}"
    if importlib.util.find_spec(module_name) is None:
      lang = 'en_us'
      module_name = f"app.config.langs.en_us"
    # 反射
    controller_module = importlib.import_module(module_name)
    controller_cls = getattr(controller_module, lang)
    # 实例化
    controller = controller_cls()
    method = getattr(controller, action)
    if argv: return method%(argv)
    else: return method

  # 返回JSON
  def GetJSON(self, data: str|dict='', status: int=200, header: list=[]) -> tuple :
    # Json类型
    headers = [
      ('Content-Type', 'application/json; charset=utf-8')
    ]
    headers.extend(header)
    # 语言
    if 'code' in data and 'msg' not in data:
      data['msg'] = self.GetLang('code_'+str(data['code']))
    # 返回
    return json.dumps(data).encode('utf-8'), status, headers

  # Get参数
  def Get(self, name: str):
    return self.get_raw[name][0] if name in self.get_raw else None
  
  # POST参数
  def Post(self, name: str):
    return self.post_raw[name][0] if name in self.post_raw else None
  
  # Json参数
  def Json(self):
    return self.post_raw
  def JsonName(self, param: dict, name: str):
    return param[name] if name in param else None
  
