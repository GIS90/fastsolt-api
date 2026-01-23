## 项目架构

基于Python语言研发，使用FastAPI、Pydantic、异步数据库搭建的后端APIs脚手架，备具Restful API、验证session、模板开发等功能，技术栈列表：
- Python：开发语言，基于python3.12版本开发
- FastAPI：python语言使用的web框架
- Pydantic：数据验证库
- Mysql：数据库
- Uvicorn：web服务与应用app之间的管理
- Supervisor：项目进程的启动、停止、重启等管理
  
***git clone***之后修改配置即可运行，在此基础上可进行二次开发，可以前端/后台独立。  
项目可以运行于Linux、Windows、Macos等系统上，建议使用Centos7.5，支持性较好。


> ## 运维

### 配置说明

项目配置主要有2套，位于项目的根目录etc下
- dev 测试环境
- prod 线上环境
**强调一点：**测试环境http，线上环境https。

每套配置文件夹下有2个配置文件：
  - config.toml：项目的db、log等项目开发用的所有配置，这里的log记录项目的log，关于项目相关的配置都可以在此文件进行配置
  - supervisor：项目进程管理的配置信息，部署到线上

.toml格式的配置文件是有deploy/config.py进行解析的，如果在config.toml配置文件中添加配置信息，需要在此文件进行解析添加。

### 环境搭建

  - Centos7.5系统服务器
  - Python3、mysql、supervisor等基础环境安装。
  - 安装好数据库之后，执行README.md文件中的数据库初始化模块，里面配置数据库名称、用户名、密码等（根据需求改成项目需要的）
  - 安装项目运行的环境：python install_env.py，建立项目独立的运行环境，安装了virtualenv、python、gunicorn、packages等操作，了解具体详情请参考install_env.py代码（如果执行遇到问题，直接用本机python环境部署requirements.txt包，详情见手工部署）
  - 更新web配置文件：etc/prod/config.yaml（线上）、etc/dev/config.yaml（测试），根据不同需求进行配置更改
  - cd 项目根目录：source .venv/bin/activate：激活项目环境
  - 启动项目：
    - 线上：gunicorn -c etc/prod/gunicorn.conf
    - 测试：gunicorn -c etc/dev/gunicorn.conf
    - **_手动启动：下面有介绍_**  
    如果是测试或者开发，建议使用手动启动项目，关于dev/prod中的config.yaml配置信息详情请参考配置解析说明部分
  - 选做：安装supervisor && 项目加入supervisor进行管理，项目包含了supervisord配置文件&&项目supervisorctl配置文件
  
### 手动部署

  - pip install -r requirements.txt

此程序运行于python3，其中requirements.txt项目所需要的包，已固定版本，如果使用了***install_env.py***一键式部署，则无须单独安装包。  
一键部署需要服务器有python3环境【部署前提】。

### 手动启动

手工启动项目是为了方便调试项目，在本机、服务器简述不同的启动方式。

#### 本机
1.项目根目录wsgi.py文件，开启app.run(host="0.0.0.0", port=9999, debug=True)  
2.安装好项目运行环境，***source .venv/bin/activate***启动项目运行python
3.执行sudo python wsgi.py，代码目前已写入，处于注释状态  
4.通过手动启动的项目为dev开发环境配置，可在deploy/config.py中进行默认调整（mode = os.environ.get('mode') or 'dev'）  
5.如果手动启动模式开启，在gunicorn进行启动，会error: [Errno 48] Address already in use.

注意：启动项目一定要用virtualenv安装的python环境进行启动（source .venv/bin/activate）


### 工具类方法

  - install_env.py项目一键式环境部署，前提服务器上有python3、pip，直接执行这个脚本即可
  - deploy>utils>base_class.py 基类
  - deploy>utils>command.py 命令行
  - deploy>utils>decorator.py 装饰器
  - deploy>utils>enum.py 枚举
  - deploy>utils>exception.py 异常类
  - deploy>utils>logger.py 日志
  - deploy>utils>status.py **API response JSON**
  - deploy>utils>status_msg.py **API response JSON message**
  - deploy>utils>utils.py 工具方法，任何Python（version：3）项目都适合使用
  - deploy>utils>watcher.py 监控打点
 
### delib封装包

  - deploy>delib>dtalk_lib.py   
    DingTalk Api class, it use to push message  
    采用单例模式的DingApi类，主要用请求dingTalk openApi来操作DingDing进行发消息等操作  
    目前，只支持机器人推送消息操作  
    类添加了is_avail对access token进行判断是否可用，如果不可用中止程序
  - deploy>delib>excel_lib.py   
    Excel表读取、写入工具  
    使用了xlrd、xlwt、openpyxl，Excel表格处理包进行开发的lib工具包
  - deploy>delib>file_lib.py   
    文件处理包(the file dealing lib)  
    静态工具包，适用于任何项目以及脚本
  - deploy>delib>http_lib.py    
    HTTP请求工具，基于requests
  - deploy>delib>image_lib.py    
    图片处理
  - deploy>delib>qywx_lib.py    
    企业微信消息通知  
    腾讯企业微信官网提供一整套WebHook API接口，内容相当丰富，可以实现内部、第三方等各种各样的功能
  - deploy>delib>store_lib.py    
    对象存储  
    使用了七牛（qiniu.com）面对对象存储，注册免费使用10G空间


### API请求参数类型

  - json  
    request.get_json()
  - form  
    request.form
  - 查询参数  
    request.args
  - 文件  
    request.files


> ## 开发特定点

### Excel合并与拆分

文件：deploy/utils/excel_lib.py

在开发Excel功能上，使用了openpyxl、xlwt && xlrd，但是都一些小问题，如下：
- openpyxl: 不支持.xls（老版本excel）
- xlwt、xlrd: 表格行数限制65535
只好，根据操作Excel数据文件的格式进行判断，去执行指定的方法，如果操作的数据文件包含一个.xls文件，就用xlwt、xlrd去处理，否则就用openpyxl。

### Github Issues

https://github.com/GIS90/open2lui/issues

### 特权账号

配置文件中有个ADMIN_AUTH_LIST配置，这个是记录与管理员账号相同权限的账户RTX，对所有的数据具有读取、更新、删除等操作。

> ## 其他

### supervisor

管理项目进程的启动、停止、重启等操作
安装：pip install supervisor
配置：
  - dev：etc/dev/supervisor_open2lisapi.conf
  - prod：etc/prod/supervisor_open2lisapi.conf

把指定环境的supervisor_open2lisapi.conf cp到/etc/supervisord.d/include/*下。  
项目root根目录下有supervisord.conf文件，用来配置supervisord，放在/etc/supervisord.d目录下。

### gunicorn

负责web项目进程、服务

安装：pip install gunicorn

配置：
  - dev：etc/dev/gunicorn.conf
  - prod：etc/prod/gunicorn.conf

如需特别项目启动信息，可以加入gunicorn.conf或者更改命令行gunicorn启动方式加入参数即可

### crontab

里面包含crontab定时任务，具体任务列表如下：
- auto_clear_logs.sh：日志清除任务
- mysql_backup_task.sh：数据库备份任务

crontab简单功能：
- crontab -e 编辑
- crontab -l 查看

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

### 其他

  - ~~bash_start.bash、bash_end.bash为手动方式进行项目启动与项目结束（已废弃）~~


## 模板代码

[TEMPLATE_CODE.md](https://github.com/GIS90/open2lisapi/blob/master/TEMPLATE_CODE.md)


***
***


> ## 联系方式

* ***Github:*** https://github.com/GIS90
* ***Email:*** gaoming971366@163.com
* ***Blog:*** http://pygo2.top
* ***OPENTOOL-Z:*** http://2l.pygo2.top/
* ***WeChat:*** PyGo90


Enjoy the good life everyday！！！



## 运行



### 启动方式：
方式一（uvicorn）：.venv/bin/uvicorn deploy:app --reload --host 0.0.0.0 --port 8000
方式二（python）：python startup.py


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