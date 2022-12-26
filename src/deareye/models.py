'''
Author: Flandre Scarlet i@flandrescarlet.cn
Github: https://github.com/OrientalFantasy
Date: 2022-11-24 15:21:36
LastEditors: Flandre Scarlet i@flandrescarlet.cn
LastEditTime: 2022-12-09 13:54:46
Copyright (c) 2022 by Flandre Scarlet i@flandrescarlet.cn, All Rights Reserved.
'''
from django.db import models

# 使用 python manage.py inspectdb > model.py 根据已有数据库生成类


# 用户表
class EyeUsers(models.Model):
    uid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=16)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=16, blank=True, null=True)
    mail = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=16)
    class_id = models.CharField(max_length=16, blank=True, null=True)
    s_id = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eye_users'
        unique_together = (('user_name', 'mail', 'nick_name', 's_id'),)

# 班级表
class EyeClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(unique=True, max_length=128)
    class_instructor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eye_class'

# 课程信息表
class EyeCourseInfo(models.Model):
    course_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eye_course_info'

# 课程表
class EyeSchoolTimetables(models.Model):
    class_id = models.IntegerField()
    term = models.CharField(max_length=64)
    timetable_info = models.TextField()
    teacher_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eye_school_timetables'

