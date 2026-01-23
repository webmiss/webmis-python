from core.Base import Base
from core.Controller import Controller
from core.Router import Router
import json, importlib
import urllib.parse

# WSGI服务器类
class WSGIApplication(Controller):

  __name: str = 'server'      # 名称

  # 自动执行
  def __call__(self, environ: dict, start_response: callable) -> bytes:
    # 获取请求路径
    path = environ.get('PATH_INFO', '/')
    if path == '/': path = '/home/index/index'
    module_name, controller_name, method_name, params = Router().parse_url(path)
    # Get 参数
    Controller.get_raw = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
    # Post 参数
    post_params = {}
    if environ.get('REQUEST_METHOD') == 'POST':
      content_len = int(environ.get('CONTENT_LENGTH', 0)) if environ.get('CONTENT_LENGTH', 0) else 0
      if content_len > 0:
        post_raw = environ['wsgi.input'].read(content_len).decode('utf-8')
        content_type = environ.get('CONTENT_TYPE', '')
        if 'application/x-www-form-urlencoded' in content_type:
          post_params = urllib.parse.parse_qs(post_raw)
        elif 'application/json' in content_type:
          post_params = json.loads(post_raw) if post_raw else {}
    Controller.post_raw = post_params
   
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

# 实例化
app = WSGIApplication()
