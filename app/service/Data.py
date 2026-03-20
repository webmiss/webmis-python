from core.Base import Base
from app.config.Env import Env
from app.util.Time import Time

# 数据类
class Data(Base):

  # 分区时间
  partition: dict = {
    'p2601': 1769875200,
    'p2602': 1772294400,
    'p2603': 1774972800,
    'p2604': 1777564800,
    'p2605': 1780243200,
    'p2606': 1782835200,
    'p2607': 1785513600,
    'p2608': 1788192000,
    'p2609': 1790784000,
    'p2610': 1793462400,
    'p2611': 1796054400,
    'p2612': 1798732800,
    'plast': 1798732800,
  }

  # 图片地址
  def Img(self, img: str, isTmp: bool=True) -> str:
    if img == "": return ""
    if isTmp : return Env.img_url + img
    else: return Env.img_url + img + '?' + Time.Time()

  # 图片地址-商品
  def ImgGoods(self, sku_id: str, isTmp: bool=True) -> str:
    if sku_id == "": return ""
    return self.Img(f"img/sku/{sku_id}.jpg", isTmp)