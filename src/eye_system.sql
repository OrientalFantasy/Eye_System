-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2022-12-14 17:52:56
-- 服务器版本： 5.7.39-log
-- PHP 版本： 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `eye_system`
--

-- --------------------------------------------------------

--
-- 表的结构 `eye_class`
--

CREATE TABLE `eye_class` (
  `class_id` int(10) NOT NULL COMMENT '班级ID',
  `class_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级名称',
  `class_instructor` int(10) DEFAULT NULL COMMENT '班级辅导员ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;


-- --------------------------------------------------------

--
-- 表的结构 `eye_course_info`
--

CREATE TABLE `eye_course_info` (
  `id` int(10) NOT NULL COMMENT '课程信息ID',
  `course_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '课程名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;


-- --------------------------------------------------------

--
-- 表的结构 `eye_school_timetables`
--

CREATE TABLE `eye_school_timetables` (
  `id` int(10) NOT NULL COMMENT '课程记录ID',
  `class_id` int(10) NOT NULL COMMENT '班级ID',
  `term` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学期',
  `timetable_info` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课表信息',
  `teacher_id` int(10) NOT NULL COMMENT '老师ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;


-- --------------------------------------------------------

--
-- 表的结构 `eye_users`
--

CREATE TABLE `eye_users` (
  `uid` int(10) NOT NULL COMMENT '用户ID',
  `user_name` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `name` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '姓名',
  `mail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `nick_name` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '昵称',
  `class_id` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级',
  `s_id` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学号/工号',
  `rank` int(1) NOT NULL COMMENT '权限'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

--
-- 转储表的索引
-- 

--
-- 表的索引 `eye_class`
--
ALTER TABLE `eye_class`
  ADD PRIMARY KEY (`class_id`) USING BTREE,
  ADD UNIQUE KEY `class_name` (`class_name`) USING BTREE;

--
-- 表的索引 `eye_course_info`
--
ALTER TABLE `eye_course_info`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `eye_school_timetables`
--
ALTER TABLE `eye_school_timetables`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `eye_users`
--
ALTER TABLE `eye_users`
  ADD PRIMARY KEY (`uid`) USING BTREE,
  ADD UNIQUE KEY `user_name` (`user_name`,`mail`,`nick_name`,`s_id`) USING BTREE;

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `eye_class`
--
ALTER TABLE `eye_class`
  MODIFY `class_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '班级ID', AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `eye_course_info`
--
ALTER TABLE `eye_course_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '课程信息ID', AUTO_INCREMENT=7;

--
-- 使用表AUTO_INCREMENT `eye_school_timetables`
--
ALTER TABLE `eye_school_timetables`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '课程记录ID', AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `eye_users`
--
ALTER TABLE `eye_users`
  MODIFY `uid` int(10) NOT NULL AUTO_INCREMENT COMMENT '用户ID', AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
