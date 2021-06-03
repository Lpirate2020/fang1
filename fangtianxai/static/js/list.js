const vm = new Vue({
    delimiters: ['{[', ']}'],//与django的jinjia2模板冲突更改原传值模板{{}}为{[]}
    el: '#app',
    data: {
        host: 'http://api.fangtianxia.site:8000',
        token: sessionStorage.token || localStorage.token,
        username: '',
        showlogin: false,//登录注册默认显示
        show: true,//欢迎用户默认不显示
        user_status: true,//用户在状态

    },
    mounted: function () {
        axios.get(this.host + '/test/', {//发请求查redis
            withCredentials: true//允许跨域携带cookie，需要后端也配置上
        })
            .then(response => {
                // console.log(response)//整体传值
                console.log(response.data['content1'])//数据返回
                if (response.data['content1']['user_status'] !== null) {
                    if (response.data['content1']['user_status'] === this.user_status) {//获取到的数据是user_status==true
                        // console.log(response.data['content1']['user_status']);//user_status值
                        // console.log(1);//user_status值
                        sessionStorage.clear();
                        if (undefined !== response.data['content1']['token']) {
                            localStorage.setItem('token', response.data['content1']['token']);
                            localStorage.setItem('user_id', response.data['content1']['user_id']);
                            localStorage.setItem('username', response.data['content1']['username'])

                        }

                    } else {
                        // console.log(response.data['content1']['user_status']);//user_status值
                        // console.log(response.data['content1']['token']);//user_status值
                        localStorage.clear();
                        if (undefined !== response.data['content1']['user_status']) {//其中一个值不空
                            // console.log(2);//user_status值
                            sessionStorage.setItem('token', response.data['content1']['token']);
                            sessionStorage.setItem('user_id', response.data['content1']['user_id']);
                            sessionStorage.setItem('username', response.data['content1']['username']);
                        }
                    }
                } else {
                    //清空浏览器缓存
                    sessionStorage.clear();
                    localStorage.clear();
                    // location.reload()
                }
            })
            .catch(function (response) {
                console.log(response);//发生错误时执行的代码
            })
        // 获取Session Storage（会话存储）
        const username1 = sessionStorage.getItem('username');

        // 获取local Storage（本地存储）
        const username2 = localStorage.getItem("username");
        // console.log(username1);//username
        // console.log(typeof username1);//username
        if (username1 !== null) {
            this.username = username1;
            // console.log(username1)//输出测试
            // console.log(1)
        } else {
            this.username = username2;
            // console.log(username2)//输出测试
            // console.log(2)
        }
        // console.log(sessionStorage.getItem('username'))

        // 遮盖
        if (typeof username1 === "object" && typeof username2 === "object") {//

            // showlogin: false,//不显示
            // show: true,//欢迎
            this.showlogin = !this.showlogin;
            this.show = !this.show;
        }

    },
    methods: {
        // 退出
        logout: function () {
            //清空浏览器缓存
            sessionStorage.clear();
            localStorage.clear();
            //发请求清空redis缓存
            axios.get(this.host + '/User_Redis_Del/', {//发请求查redis
                withCredentials: true//允许跨域携带cookie，需要后端也配置上
            })
                .then(response => {
                    // console.log(response.data);
                    location.reload()//刷新当前页
                })
                .catch(function (response) {
                    console.log(response);//发生错误时执行的代码
                })

        },
    }
});
