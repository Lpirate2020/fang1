var vm = new Vue({
    el: '#app',//查询标签
    data: {//定义变量
        // host:host,
        host,
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_phone: false,
        error_allow: false,
        error_sms_code: false,
        sending_flag: false,

        username: '',
        password: '',
        password2: '',
        mobile: '',
        sms_code: '',
        allow: false,

        sms_code_tip: '获取短信验证码',//a标签默认文字
        error_sms_code_message: '',//验证码错误信息提示
        error_name_message: '',//用户名是否重复存在错误提示消息
        error_phone_message: '',//手机号是否重复存在错误提示消息
    },
    methods: {//方法
        // 检查⽤户名
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name_message = '请输⼊5-20个字符的⽤户名';
                this.error_name = true;
            } else {
                this.error_name = false;
            }
            // 检查重名 后端UserCountView--》serializers中
            if (this.error_name === false) {
                //拼接发送get请求
                axios.get(this.host + '/usernames/' + this.username + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '⽤户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
        check_pwd: function () {//检验密码
            var len = this.password.length;
            this.error_password = len < 8 || len > 20;
        },
        check_cpwd: function () {//检验确认密码
            this.error_check_password = this.password !== this.password2;
        },
        // 检查⼿机号
        check_phone: function () {
            var re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone_message = '您输⼊的⼿机号格式不正确';
                this.error_phone = true;
            }
            if (this.error_phone === false) {
                axios.get(this.host + '/mobiles/' + this.mobile + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_phone_message = '⼿机号已存在';
                            this.error_phone = true;
                        } else {
                            this.error_phone = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
        check_sms_code: function () {//检验验证码是否输入
            this.error_sms_code = !this.sms_code;
        },
        check_allow: function () {//检验是否同意协议
            this.error_allow = !this.allow;

        },
        // 发送短信验证码
        send_sms_code: function () {
            if (this.sending_flag === true) {
                return;
            }
            this.sending_flag = true;
            // 校验参数，保证输⼊框有数据填写
            this.check_phone();
            if (this.error_phone === true) {
                this.sending_flag = false;
                return;
            }
            // 向后端接⼝发送请求，让后端发送短信验证码
            // axios.get('http://127.0.0.1:8000' + '/sms_codes/' + this.mobile + '/', {
            axios.get(this.host + '/sms_codes/' + this.mobile + '/', {
                responseType: 'json'
            })

                .then(response => {
                    // 表示后端发送短信成功
                    // 倒计时60秒，60秒后允许⽤户再次点击发送短信验证码的按钮
                    var num = 60;
                    // 设置⼀个计时器
                    var t = setInterval(() => {
                        if (num === 1) {
                            // 如果计时器到最后, 清除计时器对象
                            clearInterval(t);
                            // 将点击获取验证码的按钮展示的⽂本回复成原始⽂本
                            this.sms_code_tip = '获取短信验证码';
                            // 将点击按钮的onclick事件函数恢复回去
                            this.sending_flag = false;
                        } else {
                            num -= 1;
                            // 展示倒计时信息
                            this.sms_code_tip = num + '秒';
                        }
                    }, 1000, 60)
                })
                .catch(error => {
                    if (error.response.status === 400) {
                        // 展示发送短信错误提示
                        this.error_sms_code = true;
                        this.error_sms_code_message = error.response.data.message;
                    } else {
                        console.log(error.response.data);
                    }
                    this.sending_flag = false;
                })
        },
// 注册
        on_submit: function () {
            //检验事件
            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_sms_code();
            this.check_allow();

            if (this.error_name === false && this.error_password === false && this.error_check_password === false
                && this.error_phone === false && this.error_sms_code === false && this.error_allow === false)
                //检验事件通过后发送请求
            {
                axios.post(this.host + '/users/', {
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    allow: this.allow.toString()//allow是布尔类型
                }, {
                    responseType: 'json'
                })
                    .then(response => {
                        // 记录⽤户的登录状态
                        sessionStorage.clear();
                        localStorage.clear();
                        localStorage.token = response.data.token;
                        localStorage.username = response.data.username;
                        localStorage.user_id = response.data.id;
                        location.href = '/index.html';

                    })
                    .catch(error => {
                        if (error.response.status === 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code_message = error.response.data.non_field_errors[0];
                            } else {
                                this.error_sms_code_message = '数据有误';
                            }
                            this.error_sms_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
        }
    }
});
