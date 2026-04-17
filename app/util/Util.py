import json

# 常用工具
class Util:

  # Trim
  def Trim(str: str, cutset: str=None)-> str:
    if str is None : return ''
    return str.strip(cutset)
  
  # Ltrim
  def Ltrim(str: str, cutset: str=None)-> str:
    if str is None : return ''
    return str.lstrip(cutset)
  
  # Rtrim
  def Rtrim(str: str, cutset: str=None)-> str:
    if str is None : return ''
    return str.rstrip(cutset)
  
  # Lower
  def Lower(str: str):
    return str.lower()
  
  # Upper
  def Upper(str: str):
    return str.upper()
  
  # Explode
  def Explode(sep: str, str: str):
    return str.split(sep)
  
  # Implode
  def Implode(sep: str, arr: list):
    return sep.join(arr)
  
  # JsonEncode
  def JsonEncode(data: any) -> str:
    try:
      return json.dumps(data)
    except Exception as e:
      print(e)
      return ''

  # JsonDecode
  def JsonDecode(jsonStr: str) -> dict:
    try:
      return json.loads(jsonStr)
    except Exception as e:
      print(e)
      return {}
 