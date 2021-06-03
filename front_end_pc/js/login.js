var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        error_username: false,
        error_pwd: false,
        error_pwd_message: '请填写密码',
        username: '',
        password: '',
        remember: false
    },
    methods: {
        // 获取url路径参数
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
        // 检查数据
        check_username: function () {
            this.error_username = !this.username;
        },
        check_pwd: function () {
            if (!this.password) {
                this.error_pwd_message = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
            }
        },
        // 表单提交
        on_submit: function () {
            this.check_username();
            this.check_pwd();

            if (this.error_username === false && this.error_pwd === false) {//用户名与密码输入后向后端发送post请求
                axios.post(this.host + '/authorizations/', {
                    username: this.username,
                    password: this.password
                }, {
                    responseType: 'json',
                    withCredentials: true//允许跨域携带cookie，需要后端也配置上
                })
                    .then(response => {
                        // 使用浏览器本地存储保存token
                        if (this.remember) {
                            // 记住登录
                            sessionStorage.clear();
                            localStorage.token = response.data.token;
                            localStorage.user_id = response.data.user_id;
                            localStorage.username = response.data.username;
                            // 向后端发送登录成功用户的信息
                            axios.post(this.host + '/LoginSuccess/', {
                                token: localStorage.token,
                                user_id: localStorage.user_id,
                                username: localStorage.username,
                                user_status: this.remember

                            }, {
                                responseType: 'json',
                                withCredentials: true//允许跨域携带cookie，需要后端也配置上
                            })

                                .then((response) => {
                                    // console.log(response);
                                    this.response2 = response.data['content1']
                                    // console.log(this.response2);
                                })
                                .catch(function (error) {
                                    console.log(error);
                                })
                        } else {
                            // 会话存储token
                            // 未记住登录
                            localStorage.clear();
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                            // 向后端发送登录成功用户的信息
                            axios.post(this.host + '/LoginSuccess/', {
                                token: sessionStorage.token,
                                user_id: sessionStorage.user_id,
                                username: sessionStorage.username,
                                user_status: this.remember

                            }, {
                                responseType: 'json',
                                withCredentials: true//允许跨域携带cookie，需要后端也配置上
                            })

                                .then((response) => {
                                    // console.log(response);
                                    this.response2 = response.data['content1']
                                    // console.log(this.response2);
                                })
                                .catch(function (error) {
                                    console.log(error);
                                })
                        }


                        // 跳转页面
                        var return_url = this.get_query_string('next');
                        // console.log(return_url);
                        if (!return_url) {
                            return_url = '/index.html';
                            // return_url = '#';
                        }
                        location.href = return_url;
                    })
                    .catch(error => {
                        if (error.response.status === 400) {
                            this.error_pwd_message = '用户名或密码错误';
                        } else {
                            this.error_pwd_message = '服务器错误';
                        }
                        this.error_pwd = true;
                    })
            }
        },
    }
});
//发请求清空redis缓存
axios.get(this.host + '/User_Redis_Del/', {//发请求查redis
    withCredentials: true//允许跨域携带cookie，需要后端也配置上
})
    .then(response => {
        console.log(response.data);
    })
    .catch(function (response) {
        console.log(response);//发生错误时执行的代码
    })