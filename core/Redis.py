import redis
from redis.exceptions import RedisError
from core.Base import Base
from app.config.Redis import Redis as RedisCfg

class Redis(Base):

  redisPool: object = None  # 连接池
  conn: object = None       # 连接
  __name: str = 'Redis'     # 名称

  # 构造函数
  def __init__(self, name: str = "default"):
    # 配置
    cfg = RedisCfg().Config(name)
    # 连接池
    if Redis.redisPool is None: Redis.redisPool = redis.ConnectionPool(**cfg)
    # 创建连接
    if self.conn is None: self.RedisConn()

  # 获取连接
  def RedisConn(self) -> object:
    if self.conn is None:
      try:
        self.conn = redis.StrictRedis(connection_pool=Redis.redisPool)
      except RedisError as e:
        print('[ '+self.__name+' ]', e)
    return self.conn
  
  # 添加
  def Set(self, key: str, value: str) -> bool:
    if self.conn is None: return None
    self.conn.set(key, value)
    return True
  
  # 自增
  def Incr(self, key: str) -> int:
    if self.conn is None: return None
    return self.conn.incr(key)

  # 自减
  def Decr(self, key: str) -> int:
    if self.conn is None: return None
    return self.conn.decr(key)

  # 获取
  def Get(self, key: str) -> str:
    if self.conn is None: return None
    return self.conn.get(key)

  # 删除
  def Del(self, key: str) -> bool:
    if self.conn is None: return None
    self.conn.delete(key)
    return True

  # 是否存在
  def Exist(self, key: str) -> bool:
    if self.conn is None: return None
    return self.conn.exists(key)

  # 设置过期时间(秒)
  def Expire(self, key: str, time: int = 0) -> bool:
    if self.conn is None: return None
    self.conn.expire(key, time)
    return True

  # 获取过期时间(秒)
  def Ttl(self, key: str) -> int:
    if self.conn is None: return None
    return self.conn.ttl(key)

  # 获取长度
  def Len(self, key: str) -> int:
    if self.conn is None: return None
    return self.conn.llen(key)

  # 哈希(Hash)-添加
  def HSet(self, key: str, field: str, value: str) -> bool:
    if self.conn is None: return None
    self.conn.hset(key, field, value)
    return True
  
  # 哈希(Hash)-删除
  def HDel(self, key: str, field: str) -> bool:
    if self.conn is None: return None
    self.conn.hdel(key, field)
    return True

  # 哈希(Hash)-获取
  def HGet(self, key: str, field: str) -> str:
    if self.conn is None: return None
    return self.conn.hget(key, field)
  
  # 哈希(Hash)-获取全部
  def HGetAll(self, key: str) -> dict:
    if self.conn is None: return None
    return self.conn.hgetall(key)
  
  # 哈希(Hash)-获取全部字段
  def HKeys(self, key: str) -> list:
    if self.conn is None: return None
    return self.conn.hkeys(key)
  
  # 哈希(Hash)-获取全部值
  def HVals(self, key: str) -> list:
    if self.conn is None: return None
    return self.conn.hvals(key)

  # 哈希(Hash)-是否存在
  def HExist(self, key: str, field: str) -> bool:
    if self.conn is None: return None
    return self.conn.hexists(key, field)
  
  # 哈希(Hash)-获取长度
  def HLen(self, key: str) -> int:
    if self.conn is None: return None
    return self.conn.hlen(key)
