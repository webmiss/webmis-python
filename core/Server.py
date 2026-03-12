from core.Controller import Controller
from core.Router import Router
import json, importlib
import urllib.parse

# WSGI服务器类
class WSGIApplication(Controller):

  __name: str = 'Server'      # 名称

  # 自动执行
  def __call__(self, environ: dict, start_response: callable) -> bytes:
    # 允许跨域请求
    header_cors = [
      ('Access-Control-Allow-Origin', '*'),                                   # 域名
      ('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS'),    # 方法
      ('Access-Control-Allow-Headers', 'Content-Type, Content-Range, Content-Disposition, Content-Description, Authorization')
    ]
    # OPTIONS
    if environ.get('REQUEST_METHOD') == 'OPTIONS':
      header_cors.extend([('Access-Control-Max-Age', '2592000')])             # OPTIONS(缓存30天)
      start_response('200 OK', header_cors)
      return []
    # 获取请求路径
    path = environ.get('PATH_INFO', '/')
    if path == '/': path = '/web/index/index'
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
    # 缓存到控制器
    Controller.post_raw = post_params
   
    try:
      # 动态控制器类
      module_name = f"app.modules.{module_name.lower()}.{controller_name}"
      controller_module = importlib.import_module(module_name)
      controller_cls = getattr(controller_module, controller_name)
      # 实例化控制器
      controller = controller_cls()
      method = getattr(controller, method_name)
      response_body, status_code, header = method(*params)
      header_cors.extend(header)
      # 构建响应
      status = f"{status_code} OK" if status_code == 200 else f"{status_code} Error"
      start_response(status, header_cors)
      return [response_body]
    except Exception as e:
      self.Print(f"[ {self.__name} ]", str(e))
      start_response('404 Not Found OK', [('Content-Type', 'text/html; charset=utf-8')])
      return [b"404 Not Found"]

# 实例化
app = WSGIApplication()
