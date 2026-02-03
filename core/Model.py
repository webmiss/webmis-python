from pymysql import Error
from core.Base import Base
from app.config.Db import Db
from core.MySQLConnectionPool import MySQLConnectionPool

# 模型
class Model(Base):

  pool: object = None   # 连接池
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
  __keys: str = ''      # 添加-键
  __values: str = ''    # 添加-值
  __data: str = ''      # 更新-数据
  __id: int = 0         # 自增ID
  __nums: int = 0       # 影响行数

  # 获取连接
  def DBConn(self, name: str = "default") -> object :
    # 配置
    cfg = Db().Config(name)
    # 连接池
    if Model.pool is None:
      Model.pool = MySQLConnectionPool(cfg)
    # 创建连接
    if self.conn is None:
      try:
        self.conn = Model.pool.getConnection(cfg['poolMaxWait'])
      except Error as e:
        self.Print('[ '+self.__name+' ] Conn:', e)
    return self.conn
  
  # 执行SQL
  def Exec(self, conn: object, sql: str, args: tuple = ()) -> any :
    with conn.cursor() as cursor:
      try:
        cursor.execute(sql, args)
        conn.commit()
        self.__nums = cursor.rowcount
        return cursor
      except Error as e:
        self.Print('[ '+self.__name+' ] Execute:', e)
    return None

  # 关闭
  def Close(self) -> None:
    if Model.pool is not None:
      Model.pool.releaseConnection(self.conn)

  # 获取-SQL
  def GetSql(self) -> str :
    return self.__sql
  
  # 获取-自增ID
  def GetID(self) -> int:
    return self.__id
  
  # 获取-影响行数
  def GetNums(self) -> int:
    return self.__nums

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
  def Find(self, sql: str = '', args: tuple=None) :
    # SQL
    if sql == '':
      sql, args = self.SelectSQL()
      if sql == '' : return None
    # 执行
    res = []
    cs = self.Exec(self.conn, sql, args)
    if cs is None : return None
    data = cs.fetchall()
    cs.close()
    self.Close()
    # 结果
    for d in data :
      row = {}
      for i,v in enumerate(d) :
        row[cs.description[i][0]] = v
      res.append(row)
    return res

  # 查询-单条
  def FindFirst(self, sql: str = '', args: tuple=None) -> any :
    # SQL
    if sql == '':
      self.Limit(0, 1)
      sql, args = self.SelectSQL()
      if sql == '' : return None
    # 执行
    res = {}
    cs = self.Exec(self.conn, sql, args)
    if cs is None : return None
    data = cs.fetchone()
    cs.close()
    self.Close()
    # 结果
    if data is None : return None
    for i,v in enumerate(data) :
      res[cs.description[i][0]] = v
    return res

  # 添加-单条
  def Values(self, data: dict) :
    self.__args = ()
    keys, vals = [], []
    for k,v in data.items() :
      keys.append(k)
      vals.append('%s')
      self.__args += (v,)
    # 字段
    self.__keys = ','.join(keys)
    self.__values = ','.join(vals)

  # 添加-多条
  def ValuesAll(self, data: list) :
    self.__args = ()
    keys, vals, tmp = [], []
    for d in data :
      tmp = []
      for k,v in d.items() :
        keys.append(k)
        tmp.append('%s')
        self.__args += (v,)
      vals.append('('+','.join(tmp)+')')
    # 字段
    self.__keys = ','.join(keys)
    self.__values = ','.join(vals)

  # 添加-SQL
  def InsertSQL(self) -> tuple[str, tuple]:
    # 验证
    if self.__table == '' :
      self.Print('[ '+self.__name+' ]', 'Insert: 表不能为空')
      return '', ()
    if self.__keys == '' or self.__values == '' :
      self.Print('[ '+self.__name+' ]', 'Insert: 字段或值不能为空')
      return '', ()
    # SQL
    self.__sql = 'INSERT INTO '+self.__table+' ('+self.__keys+') VALUES ('+self.__values+')'
    self.__table = ''
    self.__keys = ''
    self.__values = ''
    # 参数
    args: tuple = self.__args
    self.__args = ()
    # 结果
    return self.__sql, args
  
  # 添加-执行
  def Insert(self, sql: str = '', args: tuple=None) -> int :
    if sql == '':
      sql, args = self.InsertSQL()
    cs = self.Exec(self.conn, sql, args)
    if cs is None : return 0
    self.__id = cs.lastrowid
    cs.close()
    self.Close()
    return self.__id

  # 更新-数据
  def Set(self, data: dict) :
    self.__args = ()
    vals = []
    for k,v in data.items() :
      vals.append(k+'=%s')
      self.__args += (v,)
    # 字段
    self.__data = ','.join(vals)

  # 更新-SQL
  def UpdateSQL(self) -> tuple[str, tuple]:
    # 验证
    if self.__table == '' :
      self.Print('[ '+self.__name+' ]', 'Update: 表不能为空')
      return '', ()
    if self.__data == '' :
      self.Print('[ '+self.__name+' ]', 'Update: 字段或值不能为空')
      return '', ()
    if self.__where == '' :
      self.Print('[ '+self.__name+' ]', 'Update: 条件不能为空')
      return '', ()
    # SQL
    self.__sql = 'UPDATE '+self.__table+' SET '+self.__data+self.__where
    # 重置
    self.__table = ''
    self.__data = ''
    self.__where = ''
    # 参数
    args: tuple = self.__args
    self.__args = ()
    # 结果
    return self.__sql, args

  # 更新-执行
  def Update(self, sql: str = '', args: tuple=None) -> bool :
    if sql == '':
      sql, args = self.UpdateSQL()
    cs = self.Exec(self.conn, sql, args)
    if cs is None : return False
    cs.close()
    self.Close()
    return True

  # 删除-SQL
  def DeleteSQL(self) -> tuple[str, tuple]:
    # 验证
    if self.__table == '' :
      self.Print('[ '+self.__name+' ]', 'Delete: 表不能为空')
      return '', ()
    if self.__where == '' :
      self.Print('[ '+self.__name+' ]', 'Delete: 条件不能为空')
      return '', ()
    # SQL
    self.__sql = 'DELETE FROM '+self.__table+self.__where
    # 重置
    self.__table = ''
    self.__where = ''
    # 参数
    args: tuple = self.__args
    self.__args = ()
    # 结果
    return self.__sql, args

  # 删除-执行
  def Delete(self, sql: str = '', args: tuple=None) -> bool :
    if sql == '':
      sql, args = self.DeleteSQL()
    cs = self.Exec(self.conn, sql, args)
    if cs is None : return False
    cs.close()
    self.Close()
    return True
