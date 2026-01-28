from core.Controller import Controller
from core.View import View
from app.config.Env import Env

# 网站
class Index(Controller):

  # 首页
  def Index(self):
    context: dict = {"title": Env.title, "copy": Env.copy}
    return View().render('home/index', context)