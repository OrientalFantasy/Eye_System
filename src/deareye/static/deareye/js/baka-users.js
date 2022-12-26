var $ = mdui.$;

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
    }
}
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

BakaMethod.initDark();
