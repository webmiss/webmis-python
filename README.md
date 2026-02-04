# webmis-python
采用Python + Redis + MariaDB开发的轻量级HMVC基础框架，目录结构清晰，支持CLI方式访问资料方便执行定时脚本。包括HMVC模块化管理、自动路由、CLI命令行、Socket通信、redis缓存、Token机制等功能，提供支付宝、微信、文件上传、图像处理、二维码等常用类。

## 安装
```bash
# 下载
$ git clone https://github.com/webmiss/webmis-python.git
$ cd webmis-python
# Linux、MacOS
./bash install
# Windows
.\cmd install
```

## 开发环境
```bash
# Linux、MacOS
./bash serve
# Windows
.\cmd serve
```

## 生产环境
### Ubuntu
```bash
# Nginx
apt install nginx -y
apt autoremove -y
# MariaDB
apt install mariadb-server -y
# Redis
apt install redis-server -y
# Python3
apt install python3-pymysql python3-redis python3-jwt -y
```

### Nginx
```bash
upstream python {
    server localhost:9010;
}
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}
server {
    server_name  python.webmis.vip;
    set $root_path /home/www/webmis/python/public;
    root $root_path;
    index index.html;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://python;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }
    location ~* ^/(upload|favicon.png)/(.+)$ {
        root $root_path;
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
        if ($request_method = 'OPTIONS') { return 204; }
    }

}
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
