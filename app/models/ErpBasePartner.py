from core.Model import Model
from app.util.Util import Util

# 分仓
class ErpBasePartner(Model):

  # 构造函数
  def __init__(self):
    self.DBConn('default')
    self.Table('erp_base_partner')

  # 列表
  def GetList(self, where: list=[], columns: list=['name', 'status'], order_by: str='status DESC, sort DESC, name ASC'):
    # 查询
    m = ErpBasePartner()
    m.Columns('wms_co_id', *columns)
    m.Where(Util.Implode(' AND ', where))
    m.Order(order_by)
    all = m.Find()
    # 数据
    data: dict = {}
    for v in all:
      data[v['wms_co_id']] = v
    return data