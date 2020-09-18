<!--suppress ALL -->
<template>
  <div id="log-in">
    <el-container>
      <el-header align="center">
        <!--<h1>注册账户</h1>-->
        <h1 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">注册您的账户！</h1>
      </el-header>

      <el-main>
        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="usrName-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">用户名:</h4>
            </div>
          </el-col>
          <el-col :span="12" :push="3">
            <div class="usrName-ipt" style="margin-top: 15px;">
              <el-input class="usrName" placeholder="输入您的用户名" v-model="username"
                        size="medium" clearable required/>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="passwd-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">密码:</h4>
            </div>
          </el-col>
          <el-col :span="12" :push="3">
            <div class="passwd-ipt-hide" v-if="visible" style="margin-top: 15px;">
              <el-input class="passwd" placeholder="输入您的密码" v-model="password" type="password"
                        size="medium" minlength="4" clearable required>
                <i class="el-icon-view" title="show password" @click="pwdState('show')" slot="append"/>
              </el-input>
            </div>
            <div class="passwd-ipt-show" v-else style="margin-top: 15px;">
              <el-input class="passwd" placeholder="输入您的密码" v-model="password" type="text"
                        size="medium" minlength="4" clearable required>
                <i class="el-icon-view" title="hidden" @click="pwdState('hide')" slot="append"/>
              </el-input>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="usrName-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">邮箱:</h4>
            </div>
          </el-col>
          <el-col :span="12" :push="3">
            <div class="usrName-ipt" style="margin-top: 15px;">
              <el-input class="usrName" placeholder="输入您的邮箱" v-model="email"
                        size="medium" clearable required/>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="pwdcheck-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">验证码:</h4>
            </div>
          </el-col>
          <el-col :span="6" :push="3">
            <div class="pwdcheck-ipt" style="margin-top: 15px;">
              <el-input class="pwdcheck" placeholder="输入验证码" type="text" v-model="verifyInput"
                        size="medium" minlength="4" clearable required/>
            </div>
          </el-col>
          <el-col :span="4" :push="3">
            <div class="identifybox" @click="refreshCode" style="margin-top: 15px;">
              <s-identify :identifyCode="identifyCode"></s-identify>
            </div>
          </el-col>
        </el-row>
      </el-main>

      <el-footer>
        <el-row type="flex" justify="space-around">
          <el-col :span="12" align="center">
            <div class="confirm-info">
              <el-button class="confirm-btn" type="primary" v-on:click="register" round>注册</el-button>
            </div>
          </el-col>
          <el-col :span="12" align="center">
            <div class="confirm-info">
              <el-button class="confirm-btn" type="danger" v-on:click="toHomePage" round>返回</el-button>
            </div>
          </el-col>
        </el-row>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
    import SIdentify from './verifyCode'
    import qs from 'qs';

    export default {
        components: {
            's-identify': SIdentify
        },
        data() {
            return {
                usrName: localStorage.getItem('name'),
                passwd: localStorage.getItem('password'),
                username: '',
                password: '',
                email: "",
                verifyInput: '',
                identifyCode: '',
                identifyCodes: '1234567890',
                visible: true,
            }
        },
        methods: {
            checkInfo: function () {
                console.log(this.usrName)
                console.log(this.passwd)
                if (this.username !== this.usrName) {
                    this.$alert('用户名错误！', '登录失败', {
                        confirmButtonText: '确定',
                        callback: action => {
                            this.$message({
                                type: 'error',
                                message: '请重新输入用户名'
                            })
                        },
                        showClose: false
                    })
                } else if (this.password !== this.passwd) {
                    this.$alert('密码错误！', '登录失败', {
                        confirmButtonText: '确定',
                        callback: action => {
                            this.$message({
                                type: 'error',
                                message: '请重新输入密码'
                            })
                        },
                        showClose: false
                    })
                } else if (this.verifyInput !== this.identifyCode) {
                    this.$alert('验证码错误！', '登录失败', {
                        confirmButtonText: '确定',
                        callback: action => {
                            this.$message({
                                type: 'error',
                                message: '请重新输入验证码'
                            })
                        },
                        showClose: false
                    })
                } else {
                    this.$router.push({path: '/main'})
                }
            },
            pwdState: function (data) {
                this.visible = !(data === 'show')
            },
            toHomePage: function () {
                this.$router.push({path: '/'})
            },
            toResetPwd: function () {
                this.$router.push({path: '/reset'})
            },
            randomNum: function (min, max) {
                return Math.floor(Math.random() * (max - min) + min)
            },
            refreshCode: function () {
                this.identifyCode = ''
                this.makeCode(4)
            },
            makeCode: function (l) {
                for (let i = 0; i < l; i++) {
                    this.identifyCode += this.identifyCodes[this.randomNum(0, this.identifyCodes.length)]
                }
                console.log(this.identifyCode)
            },
            register() {
                if (this.verifyInput !== this.identifyCode) {
                    this.$alert('验证码错误', '注册失败', {
                        confirmButtonText: 'confirm',
                        callback: action => {
                            this.$message({
                                type: 'error',
                                message: '请检查验证码后再试一次'
                            })
                        },
                        showClose: false
                    })
                    return
                }
                if (this.username.length === 0 || this.password.length === 0 || this.email.length === 0) {
                    this.$message(
                        {
                            type: 'error', message: '用户名、密码和邮箱不能放空'
                        });
                    return;
                }
                var _t = this;
                this.axios.get('/user/register', {
                        params: {
                            username: _t.username,
                            password: _t.password,
                            email: _t.email,
                        }
                    }
                ).then(function (res) {
                        if (res.data.code == 1) {
                            _t.$message(
                                {
                                    type: 'success', message: '注册成功!'
                                });
                            _t.$router.push({path: '/login'})
                        } else {

                            _t.$message(
                                {
                                    type: 'error', message: '用户名重复!'
                                })
                        }
                    }
                )
            }

        },
        created() {

        },
        mounted() {
            // 验证码初始化
            this.identifyCode = ''
            this.makeCode(4)
        }
    }
</script>

<style scoped>
  #sign-up {
    max-width: 800px;
    margin: 0 auto;
  }
</style>
