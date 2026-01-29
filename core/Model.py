import pymysql
from pymysql import Error
from core.Base import Base
from app.config.Db import Db

# 模型
class Model(Base):

  conn: object = None   # 连接
  __name: str = 'Model' # 名称
  __table: str = ''     # 数据表
  __columns: str = '*'  # 字段
  __where: str = ''     # 条件
  __group: str = ''     # 分组
  __having: str = ''    # 筛选
  __order: str = ''     # 排序
  __limit: str = ''     # 限制
  __args: tuple = ()    # 参数
  __sql: str = ''       # SQL语句

  # 获取连接
  def DBConn(self, name: str = "default") -> bool:
    cfg = Db().Config(name)
    if self.conn is None:
      try:
        self.conn = pymysql.connect(
          host=cfg['host'],
          port=cfg['port'],
          user=cfg['user'],
          password=cfg['password'],
          database=cfg['database'],
          charset=cfg['charset']
        )
      except Error as e:
        self.Print('[ '+self.__name+' ] Conn:', e)
    return self.conn is not None
  
  # 表
  def Table(self, table: str = '') -> None:
    self.__table = table

  # 分区
  def Partition(self, *partition: str) -> None:
    self.__table += ' PARTITION('+','.join(partition)+')'

  # 关联-INNER
  def Join(self, table: str = '', on: str = '') -> None:
    self.__table += ' INNER JOIN '+table+' ON '+on

  # 关联-LEFT
  def LeftJoin(self, table: str = '', on: str = '') -> None:
    self.__table += ' LEFT JOIN '+table+' ON '+on

  # 关联-RIGHT
  def RightJoin(self, table: str = '', on: str = '') -> None:
    self.__table += ' RIGHT JOIN '+table+' ON '+on

  # 关联-FULL
  def FullJoin(self, table: str = '', on: str = '') -> None:
    self.__table += ' FULL JOIN '+table+' ON '+on

  # 字段
  def Columns(self, *fields: str) -> None:
    self.__columns = ','.join(fields)

  # 条件
  def Where(self, where: str, *args) -> None:
    self.__where = ' WHERE '+where
    self.__args += args

  # 分组
  def Group(self, *group: str) -> None:
    self.__group = ' GROUP BY '+','.join(group)

  # 筛选
  def Having(self, having: str) -> None:
    self.__having = ' HAVING '+having

  # 排序
  def Order(self, *order: str) -> None:
    self.__order = ' ORDER BY '+','.join(order)

  # 限制
  def Limit(self, start: int, limit: int) -> None:
    self.__limit = ' LIMIT '+str(start)+','+str(limit)

  # 分页
  def Page(self, page: int, limit: int) -> None:
    self.__limit = ' LIMIT '+str((page - 1) * limit)+','+str(limit)

  # 查询-SQL
  def SelectSQL(self) -> tuple[str, tuple] :
    # 验证
    if self.__table == '' :
      self.Print('[ '+self.__name+' ]', 'Select: 表不能为空!')
      return '', ()
    if self.__columns == '' :
      self.Print('[ '+self.__name+' ]', 'Select: 字段不能为空!')
      return '', ()
    # SQL
    self.__sql = 'SELECT '+self.__columns+' FROM '+self.__table
    self.__table = ''
    self.__columns = '*'
    if self.__where != '' :
      self.__sql += self.__where
      self.__where = ''
    if self.__group != '' :
      self.__sql += self.__group
      self.__group = ''
    if self.__having != '' :
      self.__sql += self.__having
      self.__having = ''
    if self.__order != '' :
      self.__sql += self.__order
      self.__order = ''
    if self.__limit != '' :
      self.__sql += self.__limit
      self.__limit = ''
    # 参数
    args: tuple = self.__args
    self.__args = ()
    # 结果
    return self.__sql, args
  
  # 查询-多条
  def Find(self, param: tuple[str, tuple]=None) :
    sql, args = param if param is not None else self.SelectSQL()
