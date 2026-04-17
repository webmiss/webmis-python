# 公共配置
class Env:
  mode: str = ''                                 # 开发环境: dev
  title: str = 'WebMIS 3.0'                      # 项目名称
  copy: str = 'webmis.vip © 2026'               # 版权
  server_host: str = 'localhost'                 # 服务器地址
  server_port: int = 9010                        # 服务器端口
  key: str = 'e4b99adec618e653400966be536c45f8'  # 加密密钥
  password: str = '123456'                       # 默认密码
  # 资源
  root_dir: str = 'public/'                      # 根目录
  img_url: str = 'https://python.webmis.vip/'
  # Token
  admin_token_prefix: str = 'webmisAdmin'        # 前缀-Admin
  admin_token_time: int = 2*3600                 # 有效时长(2小时)
  admin_token_auto: bool = True                  # 自动续期
  admin_token_sso: bool = False                  # 单点登录
  api_token_prefix: str = 'webmisApi'            # 前缀-Api
  api_token_time: int = 7*24*3600                # 有效时长(7天)
  api_token_auto: bool = True                    # 自动续期
  api_token_sso: bool = True                     # 单点登录
