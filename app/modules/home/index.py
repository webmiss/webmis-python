from core.Controller import Controller
from core.View import View
from app.config.Env import Env

# 网站
class index(Controller):

  # 首页
  def index(self):
    context: dict = {"title": Env.title, "copy": Env.copy}
    return View().render('home/index', context)