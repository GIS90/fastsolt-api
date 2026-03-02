## 项目架构

基于Python语言研发，使用FastAPI、Pydantic、异步数据库搭建的后端APIs脚手架，备具Restful API、JWT验证、Utils、Delib（第三方工具包封装）等功能，技术栈列表：
- Python：开发语言，基于python3.12版本开发
- FastAPI：python语言使用的web框架
- Pydantic：数据验证库
- Mysql：数据库
- Uvicorn：web服务与应用app之间的管理
- Supervisor：项目进程的启动、停止、重启等管理
  
***git clone***之后修改配置即可运行，在此基础上可进行二次开发，用于后台独立运行。   
项目可以运行于Linux、Windows、Macos等系统上，建议使用Centos7.5，支持性较好。


> ## 运维

### 环境搭建
- Centos7.5系统服务器一台
- Python3、Mysql、Supervisor等基础配套的环境安装
- 安装好数据库之后，执行README.md文件中的数据库初始化模块，里面配置数据库名称、用户名、密码等（根据需求改成项目需要的）
- 安装requirements.txt需要的包，命令pip install -r requirements.txt 或者 uv sync，建议用uv管理Python版本环境
- 更新.env配置与对应的web配置文件：etc/prod.yaml（线上）、etc/dev.yaml（测试），根据不同需求进行配置更改
- 启动项目（cd 项目目录）：
  - Uvicorn方式：uvicorn deploy:app --reload --host 127.0.0.1 --port 8000
  - Python方式：python startup.py，端口在startup.py手工配置
- 选做：安装supervisor && 项目加入supervisor进行管理，项目包含了supervisord配置文件&&项目supervisorctl配置文件

### 配置说明
项目配置主要有2套，位于项目的根目录etc下，用于项目db、log等项目开发用的所有配置，具体的明细可以查看toml配置文件，有注释
- dev：测试环境
- prod：线上环境   

**强调一点**：测试环境http，线上环境https。.toml格式的配置文件是有deploy/config.py进行解析的，如果在config.toml配置文件中添加配置信息，需要在此文件进行解析添加。  
另外，supervisor_XXXX.conf是项目进程管理的配置信息，部署到线上。

### 项目目录
- deploy：项目源码
  - app：脚手架FSWebAppClass类的配置，包含exception、middleware
  - curd：数据库模型
  - delib：第三方工具包封装类
  - schema：包含数据格式定义：
    - po[API Route请求参数对象]：Parameter Object，base class：_po_base_model.py
    - dao[Modal数据访问对象]：Data Access Object，base class：_dao_base_model.py
    - dto[Modal数据传输API Route对象]：Data Transfer Object
  - service：用于写View与Modal之间的逻辑层
  - static：静态文件，集成了swagger-ui相关的文件，不然在查看接口说明的时间有时候加载失败
  - utils：常用的工具类
  - view：API路由定义
  - __init__.py：FSWebAppClass类初始化
  - config.py：解析配置文件的脚步
- etc：配置
- log：日志
- .env：具体使用哪个配置文件
- requirements.txt：项目依赖包
- startup.py：手动启动文件

### delib封装包
- dtalk_lib.py   
  DingTalk Api class, it use to push message  
  采用单例模式的DingApi类，主要用请求dingTalk openApi来操作DingDing进行发消息等操作  
  目前，只支持机器人推送消息操作  
  类添加了is_avail对access token进行判断是否可用，如果不可用中止程序
- excel_lib.py   
  Excel表读取、写入工具  
  使用了xlrd、xlwt、openpyxl，Excel表格处理包进行开发的lib工具包
- file_lib.py   
  文件处理包(the file dealing lib)  
  静态工具包，适用于任何项目以及脚本
- http_lib.py    
  HTTP请求工具，基于requests
- image_lib.py    
  图片处理
- qywx_lib.py    
  企业微信消息通知  
  腾讯企业微信官网提供一整套WebHook API接口，内容相当丰富，可以实现内部、第三方等各种各样的功能
- redis_lib.py    
  Redis客户端库类
  用于创建和管理Redis数据库连接的客户端库
- store_lib.py    
  对象存储  
  使用了七牛（qiniu.com）面对对象存储，注册免费使用10G空间

### 工具类方法
- base_class.py 基类
- command.py 命令行
- converter.py 转换器
- decorator.py 装饰器
- depend.py Depend依赖
- enumeration.py 枚举
- exception.py 异常类
- logger.py 日志
- printer.py 打印器
- status.py **API response JSON**
- status_value.py **API response JSON message**
- utils.py 工具方法，任何Python（version：3）项目都适合使用
- token.py Token


## 开发特定点

### Excel合并与拆分
> 文件：deploy/delib/excel_lib.py

在开发Excel功能上，使用了openpyxl、xlwt && xlrd，但是都一些小问题，如下：
- openpyxl: 不支持.xls（老版本excel）
- xlwt、xlrd: 表格行数限制65535
只好，根据操作Excel数据文件的格式进行判断，去执行指定的方法，如果操作的数据文件包含一个.xls文件，就用xlwt、xlrd去处理，否则就用openpyxl。

### Github Issues
https://github.com/GIS90/open2lui/issues


### 数据库
初始化SQL语句
```
-- 创建数据库 用户 授权
create database fastapi-q default character set utf8 collate utf8_general_ci;
create user 'fastapi-q'@'%' IDENTIFIED BY '3d829dd6151b80e9351261164abae1e3';
grant all on fastapi-q.* to 'fastapi-q';
flush  privileges;


-- 系统表-用户信息表
DROP TABLES IF EXISTS `xtb_sysuser`;
CREATE TABLE `xtb_sysuser` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `rtx_id` varchar(35) not null COMMENT '用户RTX-ID唯一标识',
    `md5_id` varchar(55) not null COMMENT '数据唯一标识：MD5-ID',
    `name` varchar(30) not null COMMENT '用户名称',
    `password` varchar(120) not null COMMENT '用户密码[md5加密]',
    `salt` varchar(55) COMMENT '密码盐值',
    `sex` varchar(2) COMMENT '用户性别',
    `email` varchar(55) COMMENT '用户邮箱',
    `phone` varchar(15) COMMENT '用户电话',
    `avatar` varchar(120) COMMENT '用户头像地址',
    `introduction` text COMMENT '用户描述',
    `role` varchar(120) COMMENT '用户角色engname值，关联role表，多角色用;分割',
    `department` varchar(55) COMMENT '用户部门md5-id值，关联department表',
    `create_rtx` varchar(35) COMMENT '创建用户',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

    PRIMARY KEY (`id`)
) COMMENT='系统表-用户信息表';

-- create index
CREATE UNIQUE INDEX xtb_sysuser_rtx_id_index ON xtb_sysuser (`rtx_id`);

-- insert default admin
insert into
xtb_sysuser(rtx_id, md5_id, name, `password`, salt, sex, email , phone, avatar, introduction, role, create_rtx, status)
VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', 'ADMIN系统管理员', 'e10adc3949ba59abbe56e057f20f883e', '101010', 'M', 'gaoming971366@163.com', '13051355646',
'http://pygo2.top/images/article_github.jpg', 'SUPER_ADMIN系统管理员', 'ADMIN', 'admin', FALSE);
```

## 其他

### supervisor
管理项目进程的启动、停止、重启等操作
安装：pip install supervisor
把指定环境的supervisor_XXXX.conf cp到/etc/supervisord.d/include/*下。  
项目root根目录下有supervisord.conf文件，用来配置supervisord，放在/etc/supervisord.d目录下。

### uvicorn
负责web项目进程、服务，安装：pip install uvicorn

### qiniu对象存储
官网开发手册Python API：https://developer.qiniu.com/kodo/1242/python
1.七牛API上传文件发送ProtocolError-Connection-aborted错误
解决：
1.1 找到Pyhton的第三方包qiniu config.py配置文件
https://github.com/qiniu/python-sdk/blob/master/qiniu/config.py
1.2 修改参数
```
_config = {
    'default_zone': zone.Zone(),
    'default_rs_host': RS_HOST,
    'default_rsf_host': RSF_HOST,
    'default_api_host': API_HOST,
    'default_uc_host': UC_HOST,
    'connection_timeout': 120,  # 链接超时为时间为30s
    'connection_retries': 3,  # 链接重试次数为3次
    'connection_pool': 10,  # 链接池个数为10
    'default_upload_threshold': 2 * _BLOCK_SIZE  # put_file上传方式的临界默认值
}
```
把connection_timeout连接时间由默认的30秒修改为120秒。
原因是服务器带宽不够导致上传超时。


## 联系方式

* ***Github:*** https://github.com/GIS90
* ***Email:*** gaoming971366@163.com
* ***Blog:*** http://pygo.space
* ***OPENTOOL-Z:*** http://2l.pygo.space
* ***WeChat:*** PyGo90


Enjoy the good life every day！！！

