import Vue from 'vue'
import App from './App'
import Routes from './router'
import store from './store'
import './plugins/element.js'
import echarts from 'echarts'
import 'echarts-wordcloud'
import axios from 'axios'
import VueAxios from 'vue-axios'

axios.defaults.baseURL = "http://10.250.189.198:5000/"; // 张琪来服务器
axios.defaults.withCredentials = true;


Routes.beforeEach((to, from, next) => {
  if (to.meta.required) {
    // 检查localStorage
    if (localStorage.token) {
      store.commit('set_token', localStorage.token);
      // 添加axios头部Authorized
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + store.state.token;
      next()
    } else {
      next({
        path: '/login',
      })
    }
  } else {
    next()
  }
});

Vue.config.productionTip = false;

Vue.use(VueAxios, axios);
Vue.prototype.$echarts = echarts;

new Vue({
  el: '#app',
  router: Routes,
  components: { App },
  template: '<App/>',
  store
});
