启动方式：
.venv/bin/uvicorn deploy:app --reload --host 0.0.0.0 --port 8000



SQL：
```
-- 创建数据库 用户 授权
create database fastapi-q default character set utf8 collate utf8_general_ci;
create user 'fastapi-q'@'%' IDENTIFIED BY '3d829dd6151b80e9351261164abae1e3';
grant all on fastapi-q.* to 'fastapi-q';
flush  privileges;

˙

-- 系统表-用户信息表
DROP TABLES IF EXISTS `xtb_sysuser`;
CREATE TABLE `xtb_sysuser` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `rtx_id` varchar(35) not null COMMENT '用户rtx唯一标识',
    `md5_id` varchar(55) not null COMMENT '唯一标识：MD5-ID',
    `name` varchar(30) not null COMMENT '用户名称',
    `password` varchar(120) not null COMMENT '用户密码[md5加密]',
    `sex` varchar(2) COMMENT '用户性别',
    `email` varchar(55) COMMENT '用户邮箱',
    `phone` varchar(15) COMMENT '用户电话',
    `avatar` varchar(120) COMMENT '用户头像地址',
    `introduction` text COMMENT '用户描述',
    `role` varchar(120) COMMENT '用户角色engname值，关联role表，多角色用;分割',
    `department` varchar(55) COMMENT '用户部门md5-id值，关联department表',
    `create_time` timestamp default CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_rtx` varchar(35) COMMENT '创建用户',
    `delete_time` timestamp COMMENT '删除时间',
    `delete_rtx` varchar(35) COMMENT '删除用户',
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

    PRIMARY KEY (`id`)
) COMMENT='系统表-用户信息表';

-- create index
CREATE UNIQUE INDEX xtb_sysuser_rtx_id_index ON xtb_sysuser (`rtx_id`);

-- insert default admin
insert into
xtb_sysuser(rtx_id, md5_id, name, `password`, sex, email , phone, avatar, introduction, role, create_rtx, status)
VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', 'ADMIN系统管理员', 'e10adc3949ba59abbe56e057f20f883e', 'M', 'gaoming971366@163.com', '13051355646',
'http://pygo2.top/images/article_github.jpg', 'SUPER_ADMIN系统管理员', 'ADMIN', 'admin', FALSE);
```