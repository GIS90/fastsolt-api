-- 创建数据库 用户 授权
CREATE DATABASE `fastsolt-q` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'fastsolt-q'@'%' IDENTIFIED BY '1f3c7628c5502f2638fe1b06faeeacfb';
GRANT ALL ON `fastsolt-q`.* TO 'fastsolt-q'@'%';
FLUSH PRIVILEGES;


-- 系统表-用户表
DROP TABLES IF EXISTS `xtb_user`;
CREATE TABLE `xtb_user` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `rtx_id` varchar(35) not null COMMENT 'RTX-ID唯一标识，有英文+数字组成',
    `md5_id` varchar(55) not null COMMENT '数据唯一标识：MD5-ID',
    `name` varchar(30) not null COMMENT '名称',
    `password` varchar(120) not null COMMENT '密码[md5加密]',
    `salt` varchar(55) COMMENT '密码盐值，随机MD5-ID',
    `sex` varchar(2) COMMENT '性别',
    `email` varchar(55) COMMENT '邮箱',
    `phone` varchar(15) COMMENT '电话',
    `avatar` varchar(120) COMMENT '头像地址',
    `introduction` text COMMENT '描述',
    `role` varchar(255) COMMENT '角色RTX-ID值（大写），关联role表，多角色用;分割',
    `department` varchar(55) COMMENT '部门MD5-ID值，关联department表',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

    PRIMARY KEY (`id`)
) COMMENT='系统表-用户表';

-- create index
CREATE UNIQUE INDEX xtb_user_rtx_id_index ON xtb_user (`rtx_id`);

-- insert default admin
insert into
xtb_user(rtx_id, md5_id, name, `password`, email , phone, avatar, introduction, role, create_rtx, status)
VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', 'ADMIN系统管理员', 'e10adc3949ba59abbe56e057f20f883e', 'gaoming971366@163.com', '13051355646',
'http://pygo2.top/images/article_github.jpg', 'SUPER_ADMIN系统管理员', 'ADMIN', 'admin', FALSE);

-- ---------------------------------------------------------------------------------------------------------------