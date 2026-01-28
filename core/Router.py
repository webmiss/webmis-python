# 路由
class Router:

  __name: str = 'app'           # 名称
  __module: str = 'home'        # 模块
  __controller: str = 'Index'   # 控制器
  __method: str = 'Index'       # 方法
  __params: list = []           # 参数

  # 解析URL: /模块/控制器/方法/参数1/参数2...
  def parse_url(self, path: str) -> tuple:
    # URL
    parts = path.strip('/').split('/')
    module = parts[0] if len(parts) > 0 else self.__module
    controller = parts[1][0].upper() + parts[1][1:] if len(parts) > 1 else self.__controller
    method = parts[2][0].upper() + parts[2][1:] if len(parts) > 2 else self.__method
    params = parts[3:] if len(parts) > 3 else self.__params
    # 返回
    return module, controller, method, params
