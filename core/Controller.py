import json

# 控制器
class Controller:

  # 返回JSON
  def GetJSON(self, data=''):
    return json.dumps(data).encode('utf-8'),200,[('Content-Type', 'application/json; charset=utf-8')]
