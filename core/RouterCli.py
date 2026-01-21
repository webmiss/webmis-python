import sys,importlib
from core.Base import Base

# 路由
class RouterCli(Base):

  __name: str = 'cli'           # 名称
  __controller: str = 'main'    # 控制器
  __method: str = 'index'       # 方法
  __params: list = []           # 参数

  # 解析URL: /模块/控制器/方法/参数1/参数2...
  def parse_url(self, argv: list) -> tuple:
    # URL
    controller = argv[1] if len(argv) > 1 else self.__controller
    method = argv[2] if len(argv) > 2 else self.__method
    params = argv[3:] if len(argv) > 3 else self.__params
    # 返回
    return controller, method, params
  
  # 执行
  def run(self, argv: list=sys.argv) -> None :
    controller_name, method_name, params = self.parse_url(argv)
    try:
      # 动态控制器类
      module_name = f"app.task.{controller_name.lower()}"
      controller_module = importlib.import_module(module_name)
      controller_cls = getattr(controller_module, controller_name)
      # 实例化控制器
      controller = controller_cls()
      method = getattr(controller, method_name)
      response_body = method(*params)
      self.Print(f"{response_body}")
    except Exception as e:
      self.Print(f"[ {self.__name} ]", str(e))
