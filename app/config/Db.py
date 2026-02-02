
# 数据库
class Db:

  # 配置
  def Config(self, name: str = "default") -> dict :
    data: dict = {}
    match name :
      case "default":
        data['host'] = 'localhost'                                # 主机
        data['port'] = 3306                                       # 端口
        data['user'] = 'webmis'                                   # 用户名
        data['password'] = 'e4b99adec618e653400966be536c45f8'     # 密码
        data['database'] = 'webmis'                               # 数据库
        data['charset'] = 'utf8mb4'                               # 编码
        data['autocommit'] = True                                 # 自动提交事务
        data['poolInitSize'] = 100                                # 连接池初始数量
        data['poolMaxSize'] = 150                                 # 连接池最大数量
        data['poolMaxWait'] = 3.0                                 # 获取连接等待时间( 秒 )
      case "other":
        data['host'] = 'localhost'                                # 主机
        data['port'] = 3306                                       # 端口
        data['user'] = 'webmis'                                   # 用户名
        data['password'] = '123456'                               # 密码
        data['database'] = 'webmis'                               # 数据库
        data['charset'] = 'utf8mb4'                               # 编码
        data['autocommit'] = True                                 # 自动提交事务
        data['poolInitSize'] = 100                                # 连接池初始数量
        data['poolMaxSize'] = 150                                 # 连接池最大数量
        data['poolMaxWait'] = 3.0                                 # 获取连接等待时间( 秒 )
    return data