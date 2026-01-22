import json

# 控制器
class Controller:

  # 返回JSON
  def GetJSON(self, data: str|dict='', status: int=200, header: list=[('Content-Type', 'application/json; charset=utf-8')]) -> tuple :
    return json.dumps(data).encode('utf-8'), status, header
  
