import re
import jwt
from core.Base import Base
from app.config.Env import Env


# 验证类
class Safety(Base):

  # 正则-公共
  def IsRight(name: str, value: str) -> bool :
    match name :
      case 'uname':
        return Safety.Test(r'^[a-zA-Z][a-zA-Z0-9\_\@\-\*\&]{3,15}$', value)
      case 'passwd':
        return Safety.Test(r'^[a-zA-Z0-9|_|@|-|*|&]{6,16}$', value)
      case 'tel':
        return Safety.Test(r'^1\d{10}$', value)
      case 'email':
        return Safety.Test(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value)
      case 'idcard':
        return Safety.Test(r'^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$', value)
      case _:
        return False
  
  # 正则-验证
  def Test(reg: str, value: str) -> bool :
    return True if re.match(reg, value) else False
  
  # Base64-加密
  def Encode(param: dict={}) -> str :
    try :
      token = jwt.encode(param, Env.key, algorithm='HS256')
      return bytes.decode(token) if type(token)==bytes else token
    except Exception as e :
      return None
  
  # Base64-解密
  def Decode(token: str) -> dict | None :
    try :
      return jwt.decode(token, Env.key, algorithms=['HS256'])
    except Exception as e :
      return None