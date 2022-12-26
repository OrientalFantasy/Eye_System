var BakaIndex = {
    onBGLoad: function () {
        var backgroundImage = new Image();

        backgroundImage.src = document.querySelector("#static_domain").href + "deareye/index/images/background.png";

        backgroundImage.onload = function () {
            document.querySelector("#background").classList.add("display-bg");
            document.querySelector("#background").classList.add("hidden-blur");
        };
    }
};

var app = new Vue({
    el: "#baka-index-app",

    components: {
        VueTyper: window.VueTyper.VueTyper
    },

    mounted() {
        BakaIndex.onBGLoad();
        setTimeout(this.init(), 100);
        this.initAudio();
    },

    data: () => ({
        titleArr: [],
        subtitle: "",
        subTitleArr: [],
        subTitleAnimation: [],
        time: 0,
        animation: [],
        hiddenSubTitle: true,
        loaded: false,
        disFor: false,
        animationButtons: [],
        btnTime: 0,
        buttons: [],
        audioScream: null,
        audioStare: null,
        clickStatus: false
    }),

    methods: {
        initAudio() {
            this.audioScream = new Audio();
            this.audioScream.loop = false;
            this.audioScream.src = document.querySelector(".enderman .enderman-screaming").dataset.audioScream;

            this.audioStare = new Audio();
            this.audioStare.loop = false;
            this.audioStare.src = document.querySelector(".enderman .enderman-screaming").dataset.audioStare;
        },

        endermanPlayAudio() {
            this.audioScream.play();
            this.audioStare.play();
        },

        init() {
            if (document.querySelector(".index-content-box") == null) return false;

            if (this.loaded === true) {
                this.disFor = !this.disFor;
                this.animation = [];
                this.subTitleAnimation = [];
                this.titleArr = [];
                this.subTitleArr = [];
                this.animationButtons = [];
                this.time = 0;
                this.btnTime = 0;
                this.hiddenSubTitle = true;
                this.$refs.SubTitle.classList.remove("display");
            }

            this.loaded = true;

            let title = SITE_TITLE;
            this.subtitle = SITE_SUBTITLE;
            this.buttons = SITE_LINKS;
            this.titleArr = title.split("");
            this.subTitleArr = this.subtitle.split("");

            this.$nextTick(function () {
                this.setTitleAnimation();
            });
        },

        setTitleAnimation() {
            var _this = this;

            // 预先设置 SubTitle 的高度
            this.$refs.SubTitle.style.height = this.$refs.SubTitle.offsetHeight + "px";

            this.titleArr.forEach((item, key) => {
                this.time = this.time + 100;

                if (item == " ") {
                    this.$set(this.titleArr, key, "&nbsp;");
                }

                setTimeout(() => {
                    _this.$set(_this.animation, key, "stroke");
                }, this.time);

                if (this.titleArr.length - 1 == key) {
                    this.displaySubTitle();
                }
            });
        },

        displaySubTitle() {
            var _this = this;
            this.$refs.SubTitle.classList.add("display");
            this.hiddenSubTitle = false;

            this.subTitleArr.forEach((item, key) => {
                this.time = this.time + 20;

                if (item == " ") {
                    this.$set(this.subTitleArr, key, "&nbsp;");
                }

                this.$set(this.subTitleAnimation, key, key % 2 === 0 ? "stroke-up" : "stroke-bottom");

                setTimeout(() => {
                    _this.$set(_this.subTitleAnimation, key, "");
                }, this.time);
            });

            this.LoadMore();
        },

        LoadMore() {
            var _this = this;
            setTimeout(() => {
                _this.$refs.Divider.classList.add("animation");
                setTimeout(() => {
                    _this.$nextTick(function () {
                        _this.setButtonsAnimation();
                    });
                }, 10);
            }, 300);
        },

        setButtonsAnimation() {
            var _this = this;
            this.btnTime = 250;

            this.buttons.forEach((item, key) => {
                this.btnTime = this.btnTime + 250;

                setTimeout(() => {
                    _this.$set(_this.animationButtons, key, "stroke");
                }, this.btnTime);

                if (this.buttons.length - 1 == key) {
                    setTimeout(() => {
                        _this.$refs.TitleBox.classList.add("text-shadow");
                        _this.$refs.Divider.classList.add("animation-light");
                    }, this.btnTime + 250);
                }
            });
        },

        displayBGText() {
            if (this.clickStatus) return;
            this.clickStatus = true;

            document.querySelector("footer#baka-footer .site-icon").classList.add("hidden");
            document.querySelector("footer#baka-footer .enderman").classList.add("display");

            var _this = this;
            this.endermanPlayAudio();
            setTimeout(() => {
                document.querySelector("footer#baka-footer .site-icon").classList.remove("hidden");
                document.querySelector("footer#baka-footer .enderman").classList.remove("display");
                _this.clickStatus = false;
            }, 3000);
        }
    }
});
