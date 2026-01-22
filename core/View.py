import os
from core.Base import Base

# 视图
class View(Base):

  __name: str = 'View'    # 名称

  # 渲染
  def render(self, template_name: str, context: dict={}, status: int=200, header: list=[('Content-Type', 'text/html; charset=utf-8')]) -> tuple :
    # 文件路径
    view_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/views')
    template_path: str = os.path.join(view_path, template_name+'.html')
    if not os.path.exists(template_path):
      self.Print(f"[ {self.__name} ]", f"视图不存在 {template_path}")
      return ''.encode('utf-8'), 404, header
    # 读取模板内容
    with open(template_path, "r", encoding="utf-8") as f:
      template = f.read()
    # 替换变量（{{ 变量名 }}）
    for key, value in context.items():
      # 处理列表循环（{% for ... %}）
      if isinstance(value, list) and f"{{% for {key[:-1]} in {key} %}}" in template:
        item_key = key[:-1]  # users → user
        # 截取循环块
        loop_start = template.find(f"{{% for {item_key} in {key} %}}")
        loop_end = template.find(f"{{% endfor %}}")
        loop_content = template[loop_start + len(f"{{% for {item_key} in {key} %}}"):loop_end]
        # 渲染循环内容
        rendered_loop = ""
        for item in value:
          temp = loop_content
          for k, v in item.items():
            temp = temp.replace(f"{{{{ {item_key}.{k} }}}}", str(v))
          rendered_loop += temp
        # 替换原循环块
        template = template[:loop_start] + rendered_loop + template[loop_end + len(f"{{% endfor %}}"):]
      # 替换普通变量
      template = template.replace(f"{{{{ {key} }}}}", str(value))
    # 返回
    return template.encode('utf-8'), status, header