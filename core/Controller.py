import json
from core.Base import Base

# 控制器
class Controller(Base):

  get_raw: dict = {}    # Get参数
  post_raw: dict = {}   # Post参数

  # 返回JSON
  def GetJSON(self, data: str|dict='', status: int=200, header: list=[('Content-Type', 'application/json; charset=utf-8')]) -> tuple :
    # 允许跨域请求
    header_cors = [
      ('Access-Control-Allow-Origin', '*'),
      ('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS'),
    ]
    # 合并头部
    header_cors.extend(header)
    return json.dumps(data).encode('utf-8'), status, header_cors
  
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
  
