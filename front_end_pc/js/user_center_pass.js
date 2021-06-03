const vm = new Vue({
    el: '#app',
    data: {
        host:'http://api.fangtianxia.site:8000',
        token: sessionStorage.token || localStorage.token,
        username: '',
        showlogin: false,//显示
        show: true,//欢迎
    },
    mounted: function () {

        // 获取Session Storage（会话存储）
        const username1 = sessionStorage.getItem('username');

        // 获取Session Storage（会话存储）
        const username2 = localStorage.getItem("username");

        if (username1 !== null) {
            this.username = username1;
            // console.log(username1)//输出测试
            // console.log(1)
        } else {
            this.username = username2;
            // console.log(username2)//输出测试
            // console.log(2)
        }

        // 遮盖
        if (typeof username1 === "object" && typeof username2 === "object") {
            this.showlogin = !this.showlogin;
            this.show = !this.show;
        }

    },
    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/index.html';
        },
    }
});
var vm1 = new Vue({
    el: '#change',
    data: {
        host:'http://api.fangtianxia.site:8000',
        error_ipassword: false,
        error_password: false,
        error_check_password: false,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        username: '',
        ipassword:'',
        password:'',
        password2:'',
    },
    methods: {
        check_pwd: function (){
            var len = this.password.length;
            this.error_password = len < 8 || len > 20;
        },
        check_cpwd: function (){
            this.error_check_password = this.password !== this.password2;
        },
        // 表单提交,修改密码方法
        on_submit: function(){
            // console.log(2)
            // this.check_username();
            // this.check_ipwd();
            this.check_pwd();
            this.check_cpwd();
            if (this.error_password === false && this.error_check_password === false) {
                axios.post(this.host+'/password/',
                    // { user_id: this.user_id },
                    {
                        // 向后端传递JWT token的方法
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        ipassword: this.ipassword,
                        password: this.password,
                        password2: this.password2,
                        user_id:this.user_id,
                    }, {
                        responseType: 'json',
                        withCredentials: true
                    })
                    .then(response => {
                        // 弹出修改成功，跳转到登录页面
                        // console.log(2)
                        alert("修改成功!");
                        location.href = '/user_center_info.html'
                    })
                    .catch(error => {
                         console.log(error.response)
                        if (error.response.status === 400) {
                            alert("原始密码错误!");
                            location.href = '/user_center_pass.html'
                        } else {
                            alert('服务器错误');
                            location.href = '/user_center_pass.html'
                        }
                        this.error_pwd = true;
                    })
            }
        },

    }
});