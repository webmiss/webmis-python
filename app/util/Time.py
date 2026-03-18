import time

# 时间
class Time:

  # Time
  def Time() -> int:
    return int(time.time())
  
  # Date: %Y-%m-%d %H:%M:%S
  def Date(format: str, timestamp: int=0) -> str:
    time_tuple = time.localtime(timestamp) if timestamp>0 else time.localtime()
    return time.strftime(format, time_tuple)