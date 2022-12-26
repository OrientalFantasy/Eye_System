'''
Author: Flandre Scarlet i@flandrescarlet.cn
Github: https://github.com/OrientalFantasy
Date: 2022-10-31 15:34:25
LastEditors: Flandre Scarlet i@flandrescarlet.cn
LastEditTime: 2022-12-14 14:35:11
Copyright (c) 2022 by Flandre Scarlet i@flandrescarlet.cn, All Rights Reserved.
'''


from django.contrib import admin
from django.urls import path, include
from deareye import views
from django.views import static
from django.conf import settings


urlpatterns = [
    ############ 路由设置 ##########
    path('500', views.http_500),
    path('404', views.http_404),

    ####### 主页 ######
    path('', views.index),

    ####### 验证码 ######
    path('captcha', include('captcha.urls')),
    path('refresh_captcha', views.refresh_captcha),

    ######## 用户操作 ########
    # 用户注册
    path('register', views.register),
    # 用户登录
    path('login', views.login),
    # 用户注销登录
    path('logout', views.logout),

    ######## 用户中心 #########
    # 用户中心主页
    path('users', views.users_index),
    # 用户信息修改
    path('users/info', views.users_info),
    # 学生 课程表
    path('users/timetable', views.school_timetable),
    # 教师 学生导入
    path('users/simport', views.student_import),
    # 教师 学生名册导出
    path('users/sexport', views.student_export),
    # 教师 学生列表
    path('users/student_list', views.student_list),
    # 管理员 用户列表
    path('users/list', views.users_list),
    # 下载批量导入模板
    path('download/student', views.download_student),
]

###### 错误页 #####
# handler404 = views.http_404
# handler500 = views.http_500
