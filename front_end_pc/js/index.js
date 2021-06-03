const vm = new Vue({
    el: '#app',
    data: {
        host,
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
            console.log(username1)//输出测试
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
            //发请求清空redis缓存
            // axios.get(this.host + '/User_Redis_Del/', {//发请求查redis
            //     withCredentials: true//允许跨域携带cookie，需要后端也配置上
            // })
            //     .then(response => {
            //         console.log(response.data);
            //     })
            //     .catch(function (response) {
            //         console.log(response);//发生错误时执行的代码
            //     })
            location.href = '/index.html';
        },
    }
});
