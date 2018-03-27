# SHOW CREATE TABLE gewara_movie
# 数据库
USE `ysali`;

DROP TABLE IF EXISTS `gewara_movie`;
CREATE TABLE `gewara_movie` (
  `nm_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键；自增长ID',
  `nm_movieId` varchar(30) DEFAULT NULL COMMENT '影片ID',
  `vc_name` varchar(100) DEFAULT NULL COMMENT '影片名称',
  `vc_nameEn` varchar(100) DEFAULT NULL COMMENT '英文名称',
  `vc_summary` varchar(1000) DEFAULT NULL COMMENT '摘要',
  `vc_tag` varchar(100) DEFAULT NULL COMMENT '标签',
  `vc_pic` varchar(1000) DEFAULT NULL COMMENT '图片',
  `vc_director` varchar(100) DEFAULT NULL COMMENT '导演',
  `vc_actors` varchar(2000) DEFAULT NULL COMMENT '演员',
  `vc_type` varchar(100) DEFAULT NULL COMMENT '类型',
  `vc_country` varchar(100) DEFAULT NULL COMMENT '国家',
  `vc_language` varchar(100) DEFAULT NULL COMMENT '语言',
  `vc_runningTime` varchar(100) DEFAULT NULL COMMENT '时长',
  `dt_releaseDate` varchar(64) DEFAULT NULL COMMENT '发布日期',
  `vc_story` varchar(4000) DEFAULT NULL COMMENT '剧情',
  `dt_create` datetime DEFAULT NULL COMMENT '采集时间',
  `dt_update` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`nm_id`),
  UNIQUE KEY `nm_movieId` (`nm_movieId`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='格瓦拉_电影简介'

USE `ysali`;
DROP TABLE IF EXISTS `gewara_comment`;
CREATE TABLE `gewara_comment` (
  `nm_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `vc_movieid` varchar(100) NOT NULL COMMENT '电影id',
  `vc_moviename` varchar(100) DEFAULT NULL COMMENT '电影名称',
  `vc_commentid` varchar(100) NOT NULL COMMENT '评论id',
  `vc_commenturl` varchar(100) DEFAULT NULL COMMENT '评论url',
  `dt_pubtime` datetime DEFAULT NULL COMMENT '发布时间',
  `vc_userurl` varchar(1000) DEFAULT NULL COMMENT '用户url',
  `vc_username` varchar(100) DEFAULT NULL COMMENT '用户名',
  `vc_score` varchar(100) DEFAULT NULL COMMENT '评分',
  `vc_commenttitle` varchar(4000) DEFAULT NULL COMMENT '评论标题',
  `vc_commentcontent` text COMMENT '评论内容',
  `vc_like` varchar(100) DEFAULT NULL COMMENT '赞量',
  `vc_replay` varchar(100) DEFAULT NULL COMMENT '回复数',
  `vc_ticket` varchar(100) DEFAULT NULL COMMENT '购票标签',
  `dt_create` datetime DEFAULT NULL COMMENT '创建时间',
  `dt_update` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`nm_id`),
  UNIQUE KEY `vc_movieid` (`vc_movieid`,`vc_commentid`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='格瓦拉-电影评论'

# 存储过程
DELIMITER $$

USE `ysali`$$

DROP PROCEDURE IF EXISTS `pro_add_gewara_movie`$$

CREATE PROCEDURE `pro_add_gewara_movie`(
	v_movieId INT(10),v_name varchar(100),v_nameEn varchar(100),v_summary varchar(1000),v_tag varchar(100),v_pic varchar(1000),
	v_director varchar(100),v_actors varchar(2000),v_type varchar(100),v_country varchar(100),v_language varchar(100),
	v_runningTime varchar(100),v_releaseDate varchar(64),v_story varchar(4000),v_create datetime,v_update datetime
)
BEGIN
	INSERT INTO gewara_movie (
		nm_movieId,vc_name,vc_nameEn,vc_summary,vc_tag,vc_pic,
		vc_director,vc_actors,vc_type,vc_country,vc_language,
		vc_runningTime,dt_releaseDate,vc_story,dt_create,dt_update)
		VALUES (
		v_movieId,v_name,
		v_nameEn,v_summary,v_tag,v_pic,v_director,
		v_actors,v_type,v_country,v_language,v_runningTime,
		v_releaseDate,v_story,NOW(),NOW());
END$$

DELIMITER ;

# 存储过程
DELIMITER $$

USE `ysali`$$

DROP PROCEDURE IF EXISTS `pro_add_gewara_comment`$$

CREATE PROCEDURE `pro_add_gewara_comment`(
	`v_movieid` VARCHAR(100),`v_moviename` VARCHAR(100),`v_commentid` VARCHAR(100),`v_commenturl` VARCHAR(100),`v_pubtime` DATETIME,`v_userurl` VARCHAR(1000),
	`v_username` VARCHAR(100),`v_score` VARCHAR(100),`v_commenttitle` VARCHAR(4000),`v_commentcontent` TEXT,`v_like` VARCHAR(100),
	`v_replay` VARCHAR(100),`v_ticket` VARCHAR(100),`v_create` DATETIME,`v_update` DATETIME
)
BEGIN
	INSERT INTO gewara_comment (
		vc_movieid,vc_moviename,vc_commentid,vc_commenturl,dt_pubtime,vc_userurl,
		vc_username,vc_score,vc_commenttitle,vc_commentcontent,vc_like,
		vc_replay,vc_ticket,dt_create,dt_update)
		VALUES (
		v_movieid,v_moviename,v_commentid,v_commenturl,v_pubtime,v_userurl,
		v_username,v_score,v_commenttitle,v_commentcontent,v_like,
		v_replay,v_ticket,NOW(),NOW());
END$$

DELIMITER ;