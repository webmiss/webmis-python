import random, io
from captcha.image import ImageCaptcha

# 验证码
class Captcha:

  # 字符集
  __txtChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

  # 获取字符
  def GetCode(num):
    code = ''.join(random.choice(Captcha.__txtChars) for _ in range(num))
    return code
  
  # 获取数字
  def GetNum(num):
    code = ''.join(random.choice('0123456789') for _ in range(num))
    return code
  
  # 图形验证码
  def Vcode(num: int=4):
    code = Captcha.GetCode(num)
    generator = ImageCaptcha(width=140, height=40, font_sizes=(32, 36, 40))
    image = generator.generate(code)
    img = image.read()
    return code, img