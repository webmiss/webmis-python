from wsgiref.simple_server import make_server
from core.Base import Base
from core.Router import Router
from app.config.Env import Env
import importlib

# WSGI服务器类
class WSGIServer(Base):

  __name: str = 'server'      # 名称

  # 自动执行
  def __call__(self, environ: dict, start_response: callable) -> bytes:
    # 获取请求路径
    path = environ.get('PATH_INFO', '/')
    if path == '/': path = '/home/index/index'
    module_name, controller_name, method_name, params = Router().parse_url(path)
   
    try:
      # 动态控制器类
      module_name = f"app.modules.{module_name.lower()}.{controller_name.lower()}"
      controller_module = importlib.import_module(module_name)
      controller_cls = getattr(controller_module, controller_name)
      # 实例化控制器
      controller = controller_cls()
      method = getattr(controller, method_name)
      response_body, status_code, header = method(*params)
      # 构建响应
      status = f"{status_code} OK" if status_code == 200 else f"{status_code} Error"
      start_response(status, header)
      return [response_body]
    except Exception as e:
      self.Print(f"[ {self.__name} ]", str(e))
      start_response('404 Not Found OK', [('Content-Type', 'text/html; charset=utf-8')])
      return [b"404 Not Found"]

  # 运行
  def run(self, host: str = '127.0.0.1', port: int = 8000):
    if(Env.mode=='dev'): self.Print('Local:', f"http://{host}:{port}")
    server = make_server(host, port, self)
    server.serve_forever()

