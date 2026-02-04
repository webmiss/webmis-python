# webmis-python
采用Python + Redis + MariaDB开发的轻量级HMVC基础框架，目录结构清晰，支持CLI方式访问资料方便执行定时脚本。包括HMVC模块化管理、自动路由、CLI命令行、Socket通信、redis缓存、Token机制等功能，提供支付宝、微信、文件上传、图像处理、二维码等常用类。

## 安装
```bash
$ git clone https://github.com/webmiss/webmis-python.git
$ cd webmis-python
$ ./bash install
```

## 运行
```bash
# Linux、MacOS
./bash serve
# Windows
.\cmd serve
```

## 项目结构
```plaintext
webmis-python/
├── app
│    ├── config                   // 配置文件
│    ├── librarys                 // 第三方类
│    └── modules                  // 模块
│    │    ├── admin              // 后台
│    │    ├── api                // 应用
│    │    └── home               // 网站
│    ├── task                     // 任务类
│    └── views                    // 视图文件
├── core
│    ├── Base.py                  // 基础类
│    ├── Controller.py            // 基础控制器
│    ├── Model.py                 // 基础模型
│    ├── MySQLConnectionPool.py   // MySQL 连接池
│    ├── Redis.py                 // 缓存数据库( 连接池 )
│    ├── Router.py                // HMVC 路由
│    ├── RouterCli.py             // Cli 路由
│    ├── Server.py                // Web 服务类
│    └── View.py                  // 基础视图
├── public                         // 静态资源
├── uwsgi                          // uWsgi 配置
├── bash                           // Linux/MacOS 启动脚本
├── cmd.bat                        // Windows 启动脚本
├── cli.py                         // 命令行: python cli.py 控制器 函数 参数...
├── run_dev.py                     // 热重载( 开发环境 ): python run_dev.py
└── run.py                         // Web启动文件
```
