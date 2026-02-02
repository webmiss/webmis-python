import pymysql
import queue
import threading
from typing import Optional
from core.Base import Base

# MySQL 连接池
class MySQLConnectionPool(Base):

  name: str = 'Pool'                      # 名称
  db_config: dict = {}                    # 数据库配置
  idle_connections: queue.Queue = None    # 连接队列
  total_connections: int = 0              # 已创建连接数
  max_size: int = 0                       # 最大连接数
  
  # 构造函数
  def __init__(self, cfg: dict):
    # 初始化
    if cfg['poolInitSize'] > cfg['poolMaxSize']:
      cfg['poolMaxSize'] = cfg['poolInitSize']
    # 数据库配置
    self.db_config = {
      'host': cfg['host'],
      'port': int(cfg['port']),
      'user': cfg['user'],
      'passwd': cfg['password'],
      'database': cfg['database'],
      'charset': cfg['charset'],
      'autocommit': cfg['autocommit'],
    }
    # 线程队列存储空闲连接
    self.idle_connections = queue.Queue(maxsize=cfg['poolMaxSize'])
    self.max_size = cfg['poolMaxSize']
    # 已创建连接数
    self.total_connections = 0
    self.lock = threading.Lock()
    # 初始化连接池
    for _ in range(cfg['poolInitSize']):
      conn = self._create_connection()
      if conn:
        self.idle_connections.put(conn)
        with self.lock:
          self.total_connections += 1

  # 连接数据库
  def _create_connection(self) -> Optional[pymysql.Connection]:
    try:
      return pymysql.connect(**self.db_config)
    except Exception as e:
      self.Print(f"[ {self.name} ] Error connecting to database: {e}")
      return None

  # 验证连接是否有效
  def _is_connection_valid(self, conn: pymysql.connections.Connection) -> bool:
    if conn is None:
      return False
    try:
      with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
      return True
    except pymysql.MySQLError:
      return False

  # 获取连接
  def getConnection(self, timeout: float = 5.0) -> Optional[pymysql.connections.Connection]:
    try:
      # 从空闲连接队列中获取连接
      conn = self.idle_connections.get(timeout=timeout)
      if not self._is_connection_valid(conn):
        conn.close()
        conn = self._create_connection()
      return conn
    except queue.Empty:
      # 如果队列为空，则尝试创建新的连接
      with self.lock:
        if self.total_connections < self.max_size:
          conn = self._create_connection()
          if conn:
            self.total_connections += 1
            return conn
      self.Print(f"[ {self.name} ] 连接池已满（最大{self.max_size}），获取连接超时")
      return None

  # 归还连接
  def releaseConnection(self, conn: pymysql.connections.Connection) -> None:
    if conn is None:
      return None
    try:
      # 校验连接有效性
      if not self._is_connection_valid(conn):
        conn.close()
        with self.lock: self.total_connections -= 1
        return None
      # 尝试放回队列
      if not self.idle_connections.full():
        self.idle_connections.put(conn)
      else:
        conn.close()
        with self.lock: self.total_connections -= 1
    except pymysql.MySQLError as e:
      print(f"[ {self.name} ] 归还连接失败: {e}")
      conn.close()
      try:
        conn.close()
        with self.lock: self.total_connections -= 1
      except:
        pass

  # 获取空闲连接数
  def get_idle_count(self) -> int:
    return self.idle_connections.qsize()          

  # 销毁连接池
  def destroy(self) -> None:
    while not self.idle_connections.empty():
      try:
        conn = self.idle_connections.get_nowait()
        if conn and not conn._closed: conn.close()
      except queue.Empty:
        break
      except pymysql.MySQLError as e:
        print(f"[ {self.name} ] 关闭连接失败: {e}")
    with self.lock: self.total_connections = 0
