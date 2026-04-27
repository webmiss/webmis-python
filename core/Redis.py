from core.Base import Base
from app.config.Redis import Redis as RedisCfg
import threading
import redis
from redis.exceptions import RedisError

class Redis(Base):

  pool_default: redis.ConnectionPool = None   # 连接池: default
  pool_other: redis.ConnectionPool = None     # 连接池: other
  __name: str = 'Redis'                       # 名称
  __db: str = 'default'                       # 数据库

  # 构造函数
  def __init__(self, name: str = "default"):
    # 数据库
    if name!='' : self.__db = name
    # 配置
    cfg = RedisCfg().Config(self.__db)
    # 初始化连接池
    if name=='default' and Redis.pool_default!=None : return
    if name=='other' and not Redis.pool_other!=None : return
    # 初始化锁
    self.lock = threading.Lock()
    # 创建连接池
    if name=='default' and Redis.pool_default is None: Redis.pool_default = redis.ConnectionPool(**cfg)
    if name=='other' and Redis.pool_other is None: Redis.pool_other = redis.ConnectionPool(**cfg)
    with self.lock:
      self.Print(f"[ {self.__name} ] Redis Pool:", name, cfg['max_connections'])

  # 默认连接池
  def GetIdleConnections(self)-> redis.ConnectionPool:
    if self.__db == 'default' : return Redis.pool_default
    elif self.__db == 'other' : return Redis.pool_other
    return None

  # 获取连接
  def RedisConn(self)-> object:
    idleConnections = self.GetIdleConnections()
    if idleConnections is None: return None
    # 连接
    conn = None
    try:
      conn = redis.StrictRedis(connection_pool=idleConnections)
    except RedisError as e:
      print('[ '+self.__name+' ] RedisConn:', e)
    return conn
  
  # 添加
  def Set(self, key: str, value: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.set(key, value)
    return res
  
  # 自增
  def Incr(self, key: str)-> int:
    conn = self.RedisConn()
    if conn is None: return 0
    res = conn.incr(key)
    return res if res else 0

  # 自减
  def Decr(self, key: str)-> int:
    conn = self.RedisConn()
    if conn is None: return 0
    res = conn.decr(key)
    return res if res else 0

  # 获取
  def Get(self, key: str)-> str:
    conn = self.RedisConn()
    if conn is None: return ''
    res = conn.get(key)
    return res if res is not None else ''

  # 删除
  def Del(self, key: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.delete(key)
    return True if res else False

  # 是否存在
  def Exist(self, key: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.exists(key)
    return True if res else False

  # 设置过期时间(秒)
  def Expire(self, key: str, time: int = 0)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.expire(key, time)
    return True if res else False

  # 获取过期时间(秒)
  def Ttl(self, key: str)-> int:
    conn = self.RedisConn()
    if conn is None: return 0
    res = conn.ttl(key)
    return res if res else 0

  # 获取长度
  def StrLen(self, key: str)-> int:
    conn = self.RedisConn()
    if conn is None: return 0
    res = conn.strlen(key)
    return res if res else 0

  # 哈希(Hash)-添加
  def HSet(self, key: str, field: str, value: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.hset(key, field, value)
    return True if res else False
  
  # 哈希(Hash)-删除
  def HDel(self, key: str, field: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.hdel(key, field)
    return True if res else False

  # 哈希(Hash)-获取
  def HGet(self, key: str, field: str)-> str:
    conn = self.RedisConn()
    if conn is None: return ''
    res = conn.hget(key, field)
    return res if res is not None else ''

  # 哈希(Hash)-获取全部
  def HGetAll(self, key: str)-> dict:
    conn = self.RedisConn()
    if conn is None: return None
    res = conn.hgetall(key)
    return res
  
  # 哈希(Hash)-获取全部字段
  def HKeys(self, key: str)-> list:
    conn = self.RedisConn()
    if conn is None: return None
    res = conn.hkeys(key)
    return res
  
  # 哈希(Hash)-获取全部值
  def HVals(self, key: str)-> list:
    conn = self.RedisConn()
    if conn is None: return None
    res = conn.hvals(key)
    return res

  # 哈希(Hash)-是否存在
  def HExist(self, key: str, field: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.hexists(key, field)
    return True if res else False

  # 哈希(Hash)-获取长度
  def HLen(self, key: str)-> int:
    conn = self.RedisConn()
    if conn is None: return 0
    res = conn.hlen(key)
    return res if res else 0

  # 列表(List)-添加
  def LPush(self, key: str, value: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.lpush(key, value)
    return True if res else False
  def RPush(self, key: str, value: str)-> bool:
    conn = self.RedisConn()
    if conn is None: return False
    res = conn.rpush(key, value)
    return True if res else False

  # 列表(List)-获取
  def LRange(self, key: str, start: int, end: int)-> list:
    conn = self.RedisConn()
    if conn is None: return None
    res = conn.lrange(key, start, end)
    return res
  def LPop(self, key: str)-> str:
    conn = self.RedisConn()
    if conn is None: return ''
    res = conn.lpop(key)
    return res if res is not None else ''
  def RPop(self, key: str)-> str:
    conn = self.RedisConn()
    if conn is None: return ''
    res = conn.rpop(key)
    return res if res is not None else ''
  def BLPop(self, key: str, timeout: int = 0)-> tuple:
    conn = self.RedisConn()
    if conn is None: return None
    res = conn.blpop(key, timeout)
    return res
  def BRPop(self, key: str, timeout: int = 0)-> tuple:
    conn = self.RedisConn()
    if conn is None: return None
    res = conn.brpop(key, timeout)
    return res
