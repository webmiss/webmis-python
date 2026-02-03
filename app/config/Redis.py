
# 缓存数据库
class Redis:

  # 配置
  def Config(self, name: str = "default") -> dict :
    data: dict = {}
    match name :
      case "default":
        data['host'] = 'localhost'                                # 主机
        data['port'] = 6379                                       # 端口
        data['password'] = ''                                     # 密码
        data['db'] = 0                                            # 硬盘
        data['decode_responses'] = True
        data['max_connections'] = 30                             # 连接池最大数量
        data['socket_timeout'] = 3.0                             # 连接超时( 秒 )
      case "other":
        data['host'] = 'localhost'                                # 主机
        data['port'] = 6379                                       # 端口
        data['password'] = 'e4b99adec618e653400966be536c45f8'     # 密码
        data['db'] = 0                                            # 硬盘
        data['decode_responses'] = True
        data['max_connections'] = 30                             # 连接池最大数量
        data['socket_timeout'] = 3.0                             # 连接超时( 秒 )
    return data