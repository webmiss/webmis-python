import os, sys, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 热重载
ENTRY_FILE = "run.py"
PYTHON_EXEC = sys.executable 
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
process = None
def start_process():
  global process
  if process:
    try:
      process.terminate()
      process.wait(timeout=2)
    except:
      process.kill()
  # 启动新进程
  print(f"\n[重启] 启动 {ENTRY_FILE} ...")
  process = subprocess.Popen([PYTHON_EXEC, ENTRY_FILE], cwd=PROJECT_DIR)

# 监听
class CodeChangeHandler(FileSystemEventHandler):
  # 文件变更
  def on_modified(self, event):
    if not event.is_directory and event.src_path.endswith(".py"): start_process()

# 执行
if __name__ == '__main__':
  # 热重载
  start_process()
  # 观察者
  event_handler = CodeChangeHandler()
  observer = Observer()
  observer.schedule(event_handler, path=PROJECT_DIR, recursive=True)
  observer.start()
  # 主进程
  try:
    while True: time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
    if process: process.terminate()
  observer.join()