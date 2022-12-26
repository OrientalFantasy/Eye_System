import re
import json
import codecs
import urlquote
import logging
import filetype
import pandas as pd
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from deareye.models import EyeUsers as Users
from deareye.models import EyeSchoolTimetables as Timetables
from deareye.models import EyeCourseInfo as CourseInfo
from deareye.models import EyeClass as ClassInfo

logger = logging.getLogger('log')

####### 配置 Start #######
# 站点标题
SITE_NAME = "Eye System"
# 站点域名
SITE_DOMAIN = "https://eye.badapple.pro"
# ICP备案号
ICP = "滇ICP备 19007022号-1"
# 注册设置
REGISTER_SETTING = True
# 批量导入的用户默认密码
DEFAULT_IMPORT_USER_PASSWORD = "Abc1234."
# 批量导入用户模板下载地址
IMPORT_TEMPLATE_URL = "https://7ny.mxlbs.cn/uploads/2022/12/13/LNbYCE43_student.xlsx"
####### 配置 End #######



############# 主页 Start #############
def index(req):
    return render(req, "index.html")

############# 主页 End ###############

############ 错误页 Start ############
# 404 页面
@csrf_exempt
def http_404(req, exception):
# def http_404(req):
    return render(req, "404.html")

# 500 页面
@csrf_exempt
def http_500(req):
    return render(req, "500.html")

############ 错误页 End ##############

############ 验证码 Start ############
# 创建验证码
def captcha():
    # 验证码答案
    hashkey = CaptchaStore.generate_key()
    # 验证码地址
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# 刷新验证码
@csrf_exempt
def refresh_captcha(req):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 验证验证码
def verify_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            # 是否超时
            # 致憨憨一样的我
            # if time.time() < time.mktime(time.strptime(str(get_captcha.expiration), "%Y-%m-%d %H:%M:%S.%f")):
            if datetime.now() < get_captcha.expiration:
                # 判断验证码是否匹配
                if get_captcha.response == captchaStr.lower():
                    # 如果验证码匹配
                    return True
            else:
                return False
        except:
            return False
    else:
        return False

############ 验证码 End #############

############ 用户注册登录 Start ##############

# 用户账号注册

def register(req):
    if REGISTER_SETTING:
        if req.method == "GET":
            if req.session.get("username") != None:
                return  HttpResponse("<script>alert('您已登录！正在跳转...');window.location.href='/users';</script>")
                # return redirect('/')
            return render(req, "register.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "注册"})
        elif req.method == "POST":
            # print(req.POST)
            # 验证码
            if verify_captcha(req.POST.get('code'), req.POST.get('hashkey')):
            # if True:
                # 昵称格式验证
                if re.match('^.{3,10}$', req.POST.get('nickname')):
                    # 用户名格式验证
                    if re.match('^[a-zA-Z0-9_-]{3,16}$', req.POST.get('username')):
                        # 邮箱格式验证
                        if re.match('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', req.POST.get('mail')):
                            # 密码格式验证
                            if re.match('((?=.*\d)(?=.*\D)|(?=.*[a-zA-Z])(?=.*[^a-zA-Z]))(?!^.*[\u4E00-\u9FA5].*$)^\S{8,32}$', req.POST.get('password')):
                                # 检查是否重复
                                # 昵称
                                if Users.objects.filter(nick_name = req.POST.get('nickname')):
                                    return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "昵称已被注册！"}))
                                # 用户名
                                elif Users.objects.filter(user_name = req.POST.get('username')):
                                    return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "用户名已被注册！"}))
                                # 邮箱
                                elif Users.objects.filter(mail = req.POST.get('mail')):
                                    return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "邮箱已被注册！"}))
                                else:
                                    try:
                                        Users.objects.create(
                                            user_name   =   req.POST.get('username'),
                                            password    =   make_password(req.POST.get('password')),
                                            mail        =   req.POST.get('mail'),
                                            nick_name   =   req.POST.get('nickname'),
                                            s_id        =   0,
                                            name        =   "",
                                            class_id    =   "",
                                            rank        =   0
                                        )
                                        # 日志记录
                                        logger.info("IP: " + req.META.get('REMOTE_ADDR', '获取IP失败') + " 注册成功，用户名：" + req.POST.get('username'))
                                        return HttpResponse(json.dumps({"code": 200, "url": "/login", "msg": "注册成功！正在跳转登录..."}))
                                    except Exception as err:
                                        print(err)
                                        return HttpResponse(json.dumps({"code": 500, "url": "/register", "msg": "注册失败！"}))
                            else:
                                return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "密码必须满足：8-32位，必须同时包含字母、数字、特殊符号中任意两种组合。"}))
                        else:
                            return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "邮箱格式不正确！"}))
                    else:
                        return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "用户名必须满足：3-16位，仅使用大小写字母、数字、下划线。"}))
                else:
                    return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "昵称必须满足：3-10位。"}))
            else:
                return HttpResponse(json.dumps({"code": 400, "url": "/register", "msg": "验证码错误！"}))
        else:
            return HttpResponse(json.dumps({"code": 400, "msg": "错误的请求方式"}))
    else:
        return  HttpResponse("<script>alert('注册功能已关闭');window.location.href='/';</script>")

# 用户登录
@csrf_exempt
def login(req):
    if req.method == "GET":
        # print(req.session.get("username"))
        # print(req.session.get('rank'))
        if req.session.get("username") != None:
            return  HttpResponse("<script>alert('您已登录！正在跳转...');window.location.href='/users';</script>")
        return render(req, "login.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "登录"})
    elif req.method == "POST":
        # 验证码
        # print(req.POST)
        if verify_captcha(req.POST.get('code'), req.POST.get('hashkey')):
        # if True:
            # 用户名格式验证
            if re.match('^[a-zA-Z0-9_-]{3,16}$', req.POST.get('username')):
                # 密码格式验证
                if re.match('((?=.*\d)(?=.*\D)|(?=.*[a-zA-Z])(?=.*[^a-zA-Z]))(?!^.*[\u4E00-\u9FA5].*$)^\S{8,32}$', req.POST.get('password')):
                    # 验证用户是否存在
                    if Users.objects.filter(user_name = req.POST.get('username')):
                        users = Users.objects.filter(user_name = req.POST.get('username')).first()
                        # 验证密码
                        if check_password(req.POST.get('password'), users.password):
                            # 重新计算密码
                            users.password = make_password(req.POST.get('password'))
                            users.save()
                            req.session['username'] = users.user_name
                            req.session['rank'] = users.rank
                            # 日志记录
                            logger.info("IP: " + req.META.get('REMOTE_ADDR', '获取IP失败') + " 登录成功，用户名：" + req.POST.get('username'))
                            if req.POST.get('password') == DEFAULT_IMPORT_USER_PASSWORD:
                                print(1)
                                return HttpResponse(json.dumps({"code": 250, "url": "/users/info?username=" + req.POST.get('username') + "&edit=1", "msg": "检测到您当前的密码是默认密码，十分不安全，请修改密码！5秒为您跳转到修改页面..."}))
                            else:
                                return HttpResponse(json.dumps({"code": 200, "url": "/users", "msg": "登录成功！正在跳转... "}))
                        else:
                            return HttpResponse(json.dumps({"code": 400, "url": "/login", "msg": "用户名或密码错误！"}))
                    else:
                        return HttpResponse(json.dumps({"code": 400, "url": "/login", "msg": "用户名或密码错误！"}))
                else:
                    return HttpResponse(json.dumps({"code": 400, "url": "/login", "msg": "用户名或密码错误！"}))
            else:
                return HttpResponse(json.dumps({"code": 400, "url": "/login", "msg": "用户名或密码错误！"}))
        else:
            return HttpResponse(json.dumps({"code": 400, "url": "/login", "msg": "验证码错误！"}))
    else:
        return HttpResponse(json.dumps({"code": 400, "msg": "错误的请求方式"}))

# 用户注销登录
@csrf_exempt
def logout(req):
    req.session.clear()
    return redirect('/')

############ 用户注册登录 End ############

############ 用户中心和功能 Start ###########

# 用户中心
def users_index(req):
    if req.session.get('username') != None:
        user_info = {
            "rank": req.session.get('rank')
        }
        return render(req, "users/users.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "用户中心", "user_info": user_info})
    else:
        return  HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

# 信息查看/修改
@csrf_exempt
def users_info(req):
    # 判断是否登录
    if req.session.get('username') != None:
        # 查询已登录账号是否是教师或者管理员
        if req.session.get('rank') == 1 or req.session.get('rank') == 2:
            # 通过用户名查找
            if req.GET.get('username') != None and req.GET.get('username') != "":
                # 判断用户是否存在
                if Users.objects.filter(user_name = req.GET.get('username')):
                    user = Users.objects.filter(user_name = req.GET.get('username')).first()
                else:
                    return  HttpResponse("<script>alert('未找到该用户');window.location.href='" + SITE_DOMAIN + "/users/info';</script>")
            # 通过学工号查找
            elif req.GET.get('student_id') != None and req.GET.get('student_id') != "":
                # 判断用户是否存在
                if Users.objects.filter(s_id = req.GET.get('student_id')):
                    user = Users.objects.filter(s_id = req.GET.get('student_id')).first()
                else:
                    return  HttpResponse("<script>alert('未找到该用户');window.location.href='" + SITE_DOMAIN + "/users/info';</script>")
            # 缺省返回当前用户
            else:
                user = Users.objects.filter(user_name = req.session.get('username')).first()
        else:
            user = Users.objects.filter(user_name = req.session.get('username')).first()

        user_info = {
            "student_id":   user.s_id,
            "name":         user.name,
            "user_name":    user.user_name,
            "nick_name":    user.nick_name,
            "mail":         user.mail,
            "rank":         req.session.get('rank'),
        }
        # 用于判断是否为管理用户，学生只能修改自己的信息，不能查看其他用户的信息
        if req.GET.get('username') == req.session.get('username') or req.session.get('rank') == 1 or req.session.get('rank') == 2:
            if req.method == "POST":
                # print(req.POST)
                # 昵称验证
                if req.POST.get('nickname') != None:
                    if re.match('^.{3,10}$', req.POST.get('nickname')):
                        nick_name = req.POST.get('nickname')
                    else:
                        return  HttpResponse("<script>alert('昵称必须满足：3-10位');window.history.back(-1);</script>")
                else:
                    return  HttpResponse("<script>alert('昵称不能为空！');window.history.back(-1);</script>")
                # 邮箱验证
                if req.POST.get('mail') != None:
                    if re.match('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', req.POST.get('mail')):
                        mail = req.POST.get('mail')
                else:
                    return  HttpResponse("<script>alert('邮箱不能为空！');window.history.back(-1);</script>")
                # 判断是否修改密码
                if req.POST.get('password') != None and req.POST.get('password') != "":
                    # 密码格式验证
                    if re.match('((?=.*\d)(?=.*\D)|(?=.*[a-zA-Z])(?=.*[^a-zA-Z]))(?!^.*[\u4E00-\u9FA5].*$)^\S{8,32}$', req.POST.get('password')):
                        user.password = make_password(req.POST['password'])
                    else:
                        return  HttpResponse("<script>alert('密码不符合要求！');window.history.back(-1);</script>")
                # 学生仅可修改昵称和邮箱
                user.nick_name  =   nick_name
                user.mail       =   mail
                # 老师可修改姓名和学号
                if req.session.get('rank') == 1 or req.session.get('rank') == 2:
                    user.name       =   req.POST.get('name')
                    user.s_id       =   req.POST.get('student_id')
                # 管理员可修改用户权限等级
                if req.session.get('rank') == 2 and req.POST.get('rank') != "None":
                    user.rank       =   req.POST.get('rank')
                    # print(user.rank)
                    logger.info("IP: " + req.META.get('REMOTE_ADDR', '获取IP失败') + " 修改用户：" + user.user_name + " 的权限成功，操作用户：" + req.session.get('username'))
                try:
                    user.save()
                    logger.info("IP: " + req.META.get('REMOTE_ADDR', '获取IP失败') + " 修改成功，操作用户：" + req.session.get('username') + " 被修改档案用户：" + user.user_name)
                    return HttpResponse("<script>alert('修改成功');window.location.href='" + SITE_DOMAIN + "/users/info';</script>")
                except Exception as error:
                    logger.error(error)
                    return HttpResponse("<script>alert('修改失败');window.location.href='" + SITE_DOMAIN + "/users/info';</script>")
            # 判断返回信息修改页面还是信息查看页面
            elif req.GET.get('edit') == "1":
                # 修改信息
                if req.GET.get('delete') == "1" and req.session.get('rank') == 2:
                    try:
                        user_name = req.GET.get('username')
                        user = Users.objects.filter(user_name = user_name).delete()
                        logger.info("已删除用户：" + user_name + " 操作者：" + req.session.get('username'))
                        return HttpResponse("<script>alert('已删除该用户');window.history.back(-1);</script>")
                    except Exception as error:
                        logger.error(error)
                        return HttpResponse("<script>alert('删除失败！');window.history.back(-1);</script>")
                return render(req, "users/users_info_edit.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "信息修改", "user_info": user_info})
            else:
                return render(req, "users/users_info.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "信息查看", "user_info": user_info})
        else:
            # 显示已登录账号的信息
            return render(req, "users/users_info.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "信息查看", "user_info": user_info})
    else:
        return HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

# 课程表
def school_timetable(req):
    if req.session.get('username') != None:
        user_info = {
            "rank": req.session.get('rank')
        }
        try:
            # 查询已登录用户信息
            user = Users.objects.filter(user_name = req.session.get("username")).first()
            # 根据已登录用户班级id查询课程表保存的课程id
            tab = Timetables.objects.filter(class_id = user.class_id).first()
            l = list(tab.timetable_info)
            # 查询课程信息表，替换课程id为课程名称然后交给渲染
            timetable = []
            for i in l:
                info = CourseInfo.objects.filter(id=i).first()
                timetable.append(info.course_name)
            # print(timetable)
            return render(req, "users/users_school_timetable.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "课程表", "user_info": user_info, "timetable": timetable})
        except Exception as err:
            logger.error(err)
            return  HttpResponse("<script>alert('未找到课程表...');window.history.back(-1);</script>")
    else:
        return  HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

# 教师 学生信息导入
@csrf_exempt
def student_import(req):
    if req.session.get('username') != None:
        user_info = {
            "rank": req.session.get('rank')
        }
        if req.session.get('rank') == 1 or req.session.get('rank') == 2:
            if req.method == "GET":
                return render(req, "users/users_student_import.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "学生导入", "user_info": user_info})
            elif req.method == "POST":
                file = req.FILES.get("student_table")
                if filetype.guess_mime(file) == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    try:
                        data = pd.read_excel(file)
                        names = data['name']
                        stuid = data['student_id']
                        class_name = data['class_name']
                        if len(stuid) == len(names):
                            for i in range(len(stuid)):
                                class_info = ClassInfo.objects.filter(class_name = class_name[i]).first()
                                Users.objects.create(
                                            user_name   =   stuid[i],
                                            password    =   make_password(DEFAULT_IMPORT_USER_PASSWORD),
                                            mail        =   "",
                                            nick_name   =   "",
                                            s_id        =   stuid[i],
                                            name        =   names[i],
                                            class_id    =   class_info.class_id,
                                            rank        =   0
                                        )
                            logger.info("IP: " + req.META.get('REMOTE_ADDR', '获取IP失败') + " 成功批量导入学生账号 " + str(len(stuid)) + " 个，操作用户：" + req.session.get('username'))
                            return HttpResponse("<script>alert('导入成功！');window.history.back(-1);</script>")
                    except Exception as error:
                        logger.error(error)
                        return HttpResponse("<script>alert('导入失败！请检查导入的文件是否有错误。');window.history.back(-1);</script>")
                    else:
                        return HttpResponse("<script>alert('导入失败！');window.history.back(-1);</script>")
                else:
                    return HttpResponse("<script>alert('错误的文件类型！');window.history.back(-1);</script>")
        else:
            return HttpResponse("<script>alert('您无法访问该页面！正在返回...');window.history.back(-1);</script>")
    else:
        return HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

# 教师 学生名册导出
@csrf_exempt
def student_export(req):
    if req.session.get('username') != None:
        user_info = {
            "rank": req.session.get('rank')
        }
        if req.session.get('rank') == 1 or req.session.get('rank') == 2:
            if req.method == "GET":
                teacher = Users.objects.filter(user_name = req.session.get('username')).first()
                class_list = ClassInfo.objects.filter(class_instructor = teacher.uid)
                teacher_class_list = []
                for i in class_list:
                    teacher_class_list.append(i.class_name)
                # print(teacher_class_list)
                return render(req, "users/users_student_export.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "学生名册导出", "user_info": user_info, "teacher_class_list": teacher_class_list})

            elif req.method == "POST":
                class_name = req.POST.get("class_name")
                class_info = ClassInfo.objects.filter(class_name = class_name).first()
                users = Users.objects.filter(class_id = class_info.class_id)
                name_list = []
                s_id_list = []
                mail_list = []
                for i in users:
                    name_list.append(i.name)
                    s_id_list.append(i.s_id)
                    mail_list.append(i.mail)
                stu_list = []
                for i in range(len(name_list)):
                    info_list = []
                    info_list.append(s_id_list[i])
                    info_list.append(name_list[i])
                    info_list.append(mail_list[i])
                    info_list.append(class_name)
                    stu_list.append(info_list)
                table = pd.DataFrame(stu_list, columns=['学号', '姓名', '邮箱', '班级'])
                # 创建一个IO流对象
                output = BytesIO()
                # 初始化一个writer，传入IO对象
                writer = pd.ExcelWriter(output)
                table.to_excel(writer, "Student.xlsx", index=False)
                # 重新定位到开始
                output.seek(0)
                # 将Excel文件内容保存到IO中
                writer.save()
                # 返回给前端
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                # 写入BOM防止文件编码出错
                response.write(codecs.BOM_UTF8)
                # 直接从IO中获取数据
                response.content = output.getvalue()
                # 用urlquote解决中文文件名的问题
                file_name = str(urlquote.quote(class_name + ".xlsx"), "utf-8")
                response['Content-Disposition'] = 'attachment; filename=%s' % file_name
                return response
            else:
                return HttpResponse(json.dumps({"code": 400, "msg": "错误的请求方式"}))
        else:
            return HttpResponse("<script>alert('您无法访问该页面！正在返回...');window.history.back(-1);</script>")
    else:
        return HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

# 下载批量导入学生模板
def download_student(req):
    return redirect(IMPORT_TEMPLATE_URL)

# 教师 学生列表
def student_list(req):
    if req.session.get('username') != None:
        user_info = {
            "rank": req.session.get('rank')
        }
        if req.session.get('rank') == 1 or req.session.get('rank') == 2:
            teacher = Users.objects.filter(user_name = req.session.get('username')).first()
            teacher_id = teacher.uid
            class_list = ClassInfo.objects.filter(class_instructor = teacher_id)
            stu_name_list = []
            stu_id_list = []
            stu_class_list = []
            for i in class_list:
                # print("class id :",i.class_id)
                users = Users.objects.filter(class_id = i.class_id)
                # print(users[0].user_name)
                for j in users:
                    stu_name_list.append(j.name)
                    stu_id_list.append(j.s_id)
                    stu_class_list.append(i.class_name)
            students_info = zip(stu_name_list, stu_id_list, stu_class_list)
            return render(req, "users/users_student_list.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "学生列表", "user_info": user_info, "students_info": students_info})
        else:
            return HttpResponse("<script>alert('您无法访问该页面！正在返回...');window.history.back(-1);</script>")
    else:
        return HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

# 管理员 用户列表
def users_list(req):
    if req.session.get('username') != None:
        user_info = {
            "rank": req.session.get('rank')
        }
        if req.session.get('rank') == 2:
            users = Users.objects.all()
            uid_arr = []
            user_name_arr = []
            s_id_arr = []
            for i in range(len(users)):
                uid_arr.append(users[i].uid)
                user_name_arr.append(users[i].user_name)
                s_id_arr.append(users[i].s_id)
            users_info = zip(uid_arr, user_name_arr, s_id_arr)
            return render(req, "users/users_list.html", {"site_name": SITE_NAME, "icp": ICP, "site_domain": SITE_DOMAIN, "title": "用户管理", "user_info": user_info, "users_info": users_info})
        else:
            return HttpResponse("<script>alert('您无法访问该页面！正在返回...');window.history.back(-1);</script>")
    else:
        return HttpResponse("<script>alert('您未登录！正在跳转登录...');window.location.href='/login';</script>")

############ 用户中心和功能 End ###########
