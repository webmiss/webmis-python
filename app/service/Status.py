# 状态
class Status:

  # 公共
  def Public(name: str) -> dict :
    data: dict = {}
    match name :
      case "role_name":
        data = {'0':'用户', '1':'开发'}
      case "status_name":
        data = {'0':'禁用', '1':'正常'}
    return data