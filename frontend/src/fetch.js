import axios from 'axios'

// 创建axios实例
const service = axios.create({
  // node环境的不同，对应不同的baseURL
  // baseURL: "http://47.101.140.135:5000/",  // 学长服务器
  baseURL: "http:/10.249.215.7:5000/", // 张琪来服务器
  timeout: 5000, // 请求的超时时间
  //设置默认请求头，使post请求发送的是formdata格式数据// axios的header默认的Content-Type好像是'application/json;charset=UTF-8',我的项目都是用json格式传输，如果需要更改的话，可以用这种方式修改
  // headers: {
  // "Content-Type": "application/x-www-form-urlencoded"
  // },
  withCredentials: true // 允许携带cookie
})

// 发送请求前处理request的数据
axios.defaults.transformRequest = [function (data) {
  let newData = ''
  for (let k in data) {
    newData += encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) + '&'
  }
  return newData
}]

// request拦截器
service.interceptors.request.use(
  config => {
    // 发送请求之前，要做的业务
    return config
  },
  error => {
    // 错误处理代码

    return Promise.reject(error)
  }
)

// response拦截器
service.interceptors.response.use(
  response => {
    // 数据响应之后，要做的业务
    return response
  },
  error => {
    return Promise.reject(error)
  }
)

export default service
