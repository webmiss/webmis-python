import time
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

# 时间
class Time:

  # Time
  def Time() -> int:
    return int(time.time())
  
  # Date: Y-m-d H:i:s
  def Date(format: str, timestamp=0) -> str:
    dt = datetime.now() if timestamp==0 else datetime.fromtimestamp(int(timestamp))
    replacer = {
      "Y": f"{dt.year:04d}",
      "y": f"{dt.year:02d}"[-2:],
      "m": f"{dt.month:02d}",
      "n": f"{dt.month}",
      "d": f"{dt.day:02d}",
      "j": f"{dt.day}",
      "H": f"{dt.hour:02d}",
      "h": f"{dt.hour % 12:02d}" if dt.hour%12 !=0 else "12",
      "i": f"{dt.minute:02d}",
      "s": f"{dt.second:02d}",
      "a": "am" if dt.hour < 12 else "pm",
    }
    # 替换格式
    res = []
    for char in format:
      res.append(replacer.get(char, char))
    return "".join(res)

  # StrToTime
  def StrToTime(date_time="now", timestamp=None)-> int:
    if timestamp is not None:
      dt = datetime.fromtimestamp(int(timestamp))
    else:
      dt = parser.parse(date_time)
    return int(dt.timestamp())
    
