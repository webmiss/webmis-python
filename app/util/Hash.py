import hashlib

# 哈希
class Hash:
  
  # MD5
  def Md5(str: str) -> str:
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()