from core.Base import Base
from app.config.Db import Db
import queue
import threading
import pymysql

# MySQL 连接池
class MySQLConnectionPool(Base):

  name: str = 'MariaDB'                   # 名称
  pool_default: queue.Queue = None        # 连接池: default
  pool_other: queue.Queue = None          # 连接池: other
  __db: str = 'default'                   # 数据库
  __db_config: dict = {}                  # 数据库配置
  __max_size: int = 0                     # 最大连接数
  __maxWait: int = 3                      # 最大等待时间( 秒 )

  # 数据源
  def InitPool(self, name: str):
    self.__db = name
    # 配置
    config = Db().Config(name)
    self.__max_size = config['poolMaxSize']
    self.__db_config = {
      'host': config['host'],
      'port': int(config['port']),
      'user': config['user'],
      'passwd': config['password'],
      'database': config['database'],
      'charset': config['charset'],
      'autocommit': config['autocommit'],
    }
    # 初始化连接池
    if name=='default' and MySQLConnectionPool.pool_default!=None : return
    if name=='other' and not MySQLConnectionPool.pool_other!=None : return
    # 初始化锁
    self.lock = threading.Lock()
    # 创建连接池
    if name=='default' : MySQLConnectionPool.pool_default = queue.Queue(maxsize=self.__max_size)
    if name=='other' : MySQLConnectionPool.pool_other = queue.Queue(maxsize=self.__max_size)
    # 初始化连接数
    for _ in range(config['poolInitSize']):
      conn = self.CreateConnection()
      if conn:
        if name=='default' : MySQLConnectionPool.pool_default.put(conn)
        if name=='other' : MySQLConnectionPool.pool_other.put(conn)
    with self.lock:
      self.Print(f"[ {self.name} ] MariaDB Pool:", name, self.GetIdleCount())

  # 创建连接
  def CreateConnection(self) -> pymysql.Connection:
    try:
      return pymysql.connect(**self.__db_config)
    except Exception as e:
      self.Print(f"[ {self.name} ] CreateConnection:", e)

  # 默认连接池
  def GetIdleConnections(self) -> queue.Queue:
    if self.__db == 'default' : return MySQLConnectionPool.pool_default
    elif self.__db == 'other' : return MySQLConnectionPool.pool_other
    return None

  # 获取连接
  def GetConnection(self) -> pymysql.Connection:
    idle = self.GetIdleConnections()
    if idle is None: return None
    # 连接
    conn = None
    try:
      conn = idle.get(timeout=self.__maxWait)
      if conn.open and conn.ping(reconnect=False) is None:
        return conn
      else:
        conn.close()
      # 创建连接
      if self.GetIdleCount() < self.__max_size:
        newConn = self.CreateConnection()
        return newConn
      else:
        raise Exception(f"[ {self.name} ] Connection pool is full, timeout while acquiring idle connection.")
    except Exception as e:
      self.Print(f"[ {self.name} ] GetConnection: {e}")
    return conn

  # 归还连接
  def ReleaseConnection(self, conn: pymysql.Connection) -> bool:
    idle = self.GetIdleConnections()
    if idle is None: return False
    try:
      if conn.open and conn.ping(reconnect=False) is None:
        idle.put(conn)
      else:
        conn.close()
    except Exception as e:
      self.Print(f"[ {self.name} ] ReleaseConnection: {e}")
    return True

  # 获取空闲连接数
  def GetIdleCount(self) -> int:
    idle = self.GetIdleConnections()
    if idle is None: return 0
    return idle.qsize()
  
  # 销毁连接池
  def Destroy(self) -> None:
    try:
      # 连接池: default
      while not MySQLConnectionPool.pool_default.empty():
        conn = MySQLConnectionPool.pool_default.get()
        if conn is not None: conn.close()
      MySQLConnectionPool.pool_default = None
      # 连接池: other
      while not MySQLConnectionPool.pool_other.empty():
        conn = MySQLConnectionPool.pool_other.get()
        if conn is not None: conn.close()
      MySQLConnectionPool.pool_other = None
    except Exception as e:
      self.Print(f"[ {self.name} ] Destroy: {e}")
