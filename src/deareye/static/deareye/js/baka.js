var $ = mdui.$;

var BakaData = {
    loadingCaptcha: false,
    checkData: {}
};

var BakaMethod = {
    initDark: function () {
        const bodyClass = document.body.classList;

        if (BakaCookie.get("dark_theme") == "true") {
            bodyClass.add("baka-theme-dark");
            bodyClass.add("mdui-theme-layout-dark");
        }
    },

    darkMode: function () {
        const bodyClass = document.body.classList;

        if (bodyClass.contains("baka-theme-dark")) {
            bodyClass.remove("baka-theme-dark");
            bodyClass.remove("mdui-theme-layout-dark");
            BakaCookie.del("dark_theme");
        } else {
            bodyClass.add("baka-theme-dark");
            bodyClass.add("mdui-theme-layout-dark");
            BakaCookie.set("dark_theme", "true");
        }
    },

    /* 刷新验证码 */
    refreshCaptcha: function () {
        // 如果还在请求中则禁止继续请求
        if (BakaData.loadingCaptcha) return false;

        const submitBtn = (NOW_METHOD == "login") ? document.querySelector("button#login-btn") : document.querySelector("button#register-btn");

        var captchaBox = document.querySelector(".captcha-iamge");
        if (captchaBox.classList.contains("loaded")) {
            captchaBox.classList.remove("loaded");
            captchaBox.querySelector(".load-spinner").style.display = "";
            //submitBtn.removeAttribute("disabled");
        }

        if (captchaBox.classList.contains("load-err")) {
            captchaBox.classList.remove("load-err");
            captchaBox.querySelector(".load-spinner").style.display = "";
            //submitBtn.removeAttribute("disabled");
        }

        const SITE_URL = window.location.protocol + "//" + window.location.host;
        $.ajax({
            method: "GET",
            url: SITE_URL + "/refresh_captcha",
            success: function (data) {
                const _data = JSON.parse(data);

                document.querySelector("input[name=hashkey]").value = _data.hashkey;

                const _now_time = Date.now();
                const _captchaImg = _data.image_url + "?t=" + _now_time;

                captchaBox.querySelector("img").src = _captchaImg;
                BakaData.loadingCaptcha = true;
                //submitBtn.setAttribute("disabled", true);

                var captchaImage = new Image();
                captchaImage.src = _captchaImg;

                captchaImage.onerror = function () {
                    BakaData.loadingCaptcha = false;
                    captchaBox.classList.add("load-err");
                    //submitBtn.removeAttribute("disabled");
                    mdui.alert('验证码加载失败，请尝试重新获取 (￣﹃￣)', '错误');
                }

                captchaImage.onload = function () {
                    BakaData.loadingCaptcha = false;
                    captchaBox.classList.add("loaded");
                    //submitBtn.removeAttribute("disabled");
                    setTimeout(function () {
                        captchaBox.querySelector(".load-spinner").style.display = "none";
                    }, 500);
                }
            }
        });
    },

    // 登录请求
    login: function () {
        if (!document.querySelector("input[name=username]").value || !document.querySelector("input[name=password]").value) {
            mdui.alert('请完整填写所需内容', '提示');
            return false;
        }

        if (!document.querySelector("input[name=code]").value) {
            mdui.alert('验证码不能为空', '提示');
            return false;
        }

        document.querySelector("button#login-btn").setAttribute("disabled", true);

        // MDUI AJAX: https://www.mdui.org/docs/jq#jq-ajax
        $.ajax({
            method: 'POST',
            url: './login',
            data: {
                csrfmiddlewaretoken: document.querySelector("input[name=csrfmiddlewaretoken]").value,
                username: document.querySelector("input[name=username]").value,
                password: document.querySelector("input[name=password]").value,
                hashkey: document.querySelector("input[name=hashkey]").value,
                code: document.querySelector("input[name=code]").value
            },
            success: function (data) {
                const _data = JSON.parse(data);
                document.querySelector("button#login-btn").removeAttribute("disabled");
                if (_data.code == 200) {
                    mdui.alert('登录成功，正在跳转中...', '提示');
                    setTimeout(function () {
                        window.location.href = _data.url
                    }, 500);
                } else if (_data.code == 250) {
                    mdui.alert(_data.msg, '警告');
                    setTimeout(function () {
                        window.location.href = _data.url
                    }, 5000);
                } else if (_data.code == 400) {
                    mdui.alert(_data.msg, '提示');
                } else {
                    mdui.alert(_data.msg, '错误');
                }
            }
        })
    },

    // 注册请求
    register: function () {
        if (!document.querySelector("input[name=nickname]").value || !document.querySelector("input[name=username]").value || !document.querySelector("input[name=mail]").value || !document.querySelector("input[name=password]").value || !document.querySelector("input[name=code]").value) {
            mdui.alert('请完整填写所需内容', '提示');
            return false;
        }

        document.querySelector("button#register-btn").setAttribute("disabled", true);

        // MDUI AJAX: https://www.mdui.org/docs/jq#jq-ajax
        $.ajax({
            method: 'POST',
            url: './register',
            data: {
                csrfmiddlewaretoken: document.querySelector("input[name=csrfmiddlewaretoken]").value,
                nickname: document.querySelector("input[name=nickname]").value,
                username: document.querySelector("input[name=username]").value,
                mail: document.querySelector("input[name=mail]").value,
                password: document.querySelector("input[name=password]").value,
                hashkey: document.querySelector("input[name=hashkey]").value,
                code: document.querySelector("input[name=code]").value,
            },
            success: function (data) {
                const _data = JSON.parse(data);
                document.querySelector("button#register-btn").removeAttribute("disabled");
                if (_data.code == 200) {
                    mdui.alert(_data.msg, '提示');
                    setTimeout(function () {
                        window.location.href = _data.url
                    }, 500);
                } else if (_data.code == 400) {
                    mdui.alert(_data.msg, '提示');
                } else {
                    mdui.alert(_data.msg, '错误');
                }
            }
        })
    },

    createErrorItem: function (name, item, regx, errMsg) {
        if (!regx.test(item.target.value)) {
            BakaData.checkData[name] = false;
            item.target.parentElement.classList.add("mdui-textfield-invalid");
            if (item.target.parentElement.querySelector(".mdui-textfield-error") == undefined) {
                var errItem = document.createElement("div");
                errItem.classList.add("mdui-textfield-error");
                item.target.parentElement.appendChild(errItem);
                item.target.parentElement.querySelector(".mdui-textfield-error").innerText = errMsg;
            }
        } else {
            BakaData.checkData[name] = true;
            item.target.parentElement.classList.remove("mdui-textfield-invalid");
        }
    },

    loginCheck: function () {
        let submitBtnCheck = function () {
            let username = BakaData.checkData["username"];
            let password = BakaData.checkData["password"];
            if ((username != undefined && username === true) && (password != undefined && password === true)) {
                document.querySelector("#login-btn").removeAttribute("disabled")
            } else {
                document.querySelector("#login-btn").setAttribute("disabled", "true");
            }
        }
        document.querySelector("input[name=username]").onchange = function (item) {
            BakaMethod.createErrorItem("username", item, /^[a-zA-Z0-9_-]{3,16}$/, "用户名必须满足：3-16位，仅使用大小写字母、数字、下划线。");
            submitBtnCheck();
        };

        document.querySelector("input[name=password]").onchange = function (item) {
            BakaMethod.createErrorItem("password", item, /((?=.*\d)(?=.*\D)|(?=.*[a-zA-Z])(?=.*[^a-zA-Z]))(?!^.*[\u4E00-\u9FA5].*$)^\S{8,32}$/, "密码必须满足：8-32位，必须同时包含字母、数字、特殊符号中任意两种组合。");
            submitBtnCheck();
        };
    },

    registerCheck: function () {
        let submitBtnCheck = function () {
            let username = BakaData.checkData["username"];
            let nickname = BakaData.checkData["nickname"];
            let mail = BakaData.checkData["mail"];
            let password = BakaData.checkData["password"];
            if ((username != undefined && username === true) && (password != undefined && password === true) && (mail != undefined && mail === true) && (nickname != undefined && nickname === true)) {
                document.querySelector("#register-btn").removeAttribute("disabled")
            } else {
                document.querySelector("#register-btn").setAttribute("disabled", "true");
            }
        }

        document.querySelector("input[name=username]").onchange = function (item) {
            BakaMethod.createErrorItem("username", item, /^[a-zA-Z0-9_-]{3,16}$/, "用户名必须满足：3-16位，仅使用大小写字母、数字、下划线。");
            submitBtnCheck();
        };

        document.querySelector("input[name=password]").onchange = function (item) {
            BakaMethod.createErrorItem("password", item, /((?=.*\d)(?=.*\D)|(?=.*[a-zA-Z])(?=.*[^a-zA-Z]))(?!^.*[\u4E00-\u9FA5].*$)^\S{8,32}$/, "密码必须满足：8-32位，必须同时包含字母、数字、特殊符号中任意两种组合。");
            submitBtnCheck();
        };

        document.querySelector("input[name=mail]").onchange = function (item) {
            BakaMethod.createErrorItem("mail", item, /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/, "邮箱格式不正确！");
            submitBtnCheck();
        };

        document.querySelector("input[name=nickname]").onchange = function (item) {
            BakaMethod.createErrorItem("nickname", item, /.{3,10}$/, "昵称必须满足：3-10位。");
            submitBtnCheck();
        };
    }
};

const BakaCookie = {
    set: (name, value, days = 3, path = "/") => {
        if (days == 0 || days == null) {
            document.cookie = name + "=" + value + ";" + "path=" + path + ";";
        } else {
            var exp = new Date();
            exp.setTime(exp.getTime() + days * 24 * 60 * 60 * 1000);
            document.cookie = name + "=" + value + ";" + "expires=" + exp.toGMTString() + ";" + "path=" + path + ";";
        }
    },

    get: (name) => {
        var name = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i].trim();
            if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
        };
        return false;
    },

    has: (name) => {
        return (BakaCookie.get(name) == false) ? false : true;
    },

    del: (name) => {
        BakaCookie.set(name, "", -1)
    }
}

BakaMethod.refreshCaptcha();
BakaMethod.initDark();
if (NOW_METHOD == "login") BakaMethod.loginCheck();
if (NOW_METHOD == "register") BakaMethod.registerCheck();
