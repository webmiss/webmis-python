from core.Controller import Controller
from app.service.TokenAdmin import TokenAdmin
from app.config.Env import Env
from app.librarys.FileEo import FileEo
from app.librarys.Upload import Upload
from app.util.Time import Time

# 文件管理
class SysFile(Controller):

  __dirRoot: str = 'upload/'

  # 列表
  def List(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    path: str = self.JsonName(json, 'path')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not path : return self.GetJSON({'code':4000})
    # 数据
    FileEo.Root = Env.root_dir + self.__dirRoot
    list = FileEo.List(path)
    # 返回
    return self.GetJSON({
      'code': 0,
      'time': Time.Date('Y-m-d H:i:s'),
      'data': {'url':self.BaseUrl(self.__dirRoot), 'list':list},
    })
  
  # 新建文件夹
  def Mkdir(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    path: str = self.JsonName(json, 'path')
    name: str = self.JsonName(json, 'name')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not path or not name : return self.GetJSON({'code':4000})
    # 数据
    FileEo.Root = Env.root_dir + self.__dirRoot
    if not FileEo.Mkdir(path+name) : return self.GetJSON({'code':5000})
    # 返回
    return self.GetJSON({'code':0})
  
  # 重命名
  def Rename(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    path: str = self.JsonName(json, 'path')
    name: str = self.JsonName(json, 'name')
    rename: str = self.JsonName(json, 'rename')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not path or not name or not rename : return self.GetJSON({'code':4000})
    # 数据
    FileEo.Root = Env.root_dir + self.__dirRoot
    if not FileEo.Rename(path+rename, path+name) : return self.GetJSON({'code':5000})
    # 返回
    return self.GetJSON({'code':0})

  # 删除
  def Remove(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    path: str = self.JsonName(json, 'path')
    data: list = self.JsonName(json, 'data')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not path or not data : return self.GetJSON({'code':4000})
    # 数据
    FileEo.Root = Env.root_dir + self.__dirRoot
    for v in data : FileEo.RemoveAll(path+v)
    # 返回
    return self.GetJSON({'code':0})
  
  # 上传
  def Upload(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    path: str = self.JsonName(json, 'path')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not path : return self.GetJSON({'code':4000})
    # 数据
    file = self.file_raw['file']
    img = Upload.File(file, {'path':self.__dirRoot+path, 'bind':None})
    if not img : return self.GetJSON({'code':5000, 'msg':'上传失败!'})
    # 返回
    return self.GetJSON({'code':0})
  
  # 下载
  def Down(self):
    # 参数
    json = self.Json()
    token: str = self.JsonName(json, 'token')
    path: str = self.JsonName(json, 'path')
    filename: str = self.JsonName(json, 'filename')
    # 验证
    msg = TokenAdmin().Verify(token, self.environ['PATH_INFO'])
    if msg != '' : return self.GetJSON({'code':4001})
    if not path or not filename : return self.GetJSON({'code':4000})
    # 数据
    FileEo.Root = Env.root_dir + self.__dirRoot
    data = FileEo.Bytes(path + filename)
    # 返回
    self.GetJSON()
    return data, 200, [('Content-Type', 'application/octet-stream')]