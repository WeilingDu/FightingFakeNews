<!--suppress ALL -->
<template>
  <div id="forget-pwd">
    <el-container>
      <el-header align="center">
        <h1 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">Reset your password!</h1>
      </el-header>

      <el-main>
        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="usrName-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">Username:</h4>
            </div>
          </el-col>
          <el-col :span="12" :push="3">
            <div class="usrName-ipt" style="margin-top: 15px;">
              <el-input class="usrName" placeholder="请输入用户名" v-model="username"
                        size="medium" clearable required />
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="pwdchg-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">New password:</h4>
            </div>
          </el-col>
          <el-col :span="12" :push="3">
            <div class="pwdchg-ipt" style="margin-top: 15px;">
              <el-input class="pwdnew" placeholder="请输入新密码" v-model="pwdNew" type="text"
                        size="medium" minlength="4" clearable required />
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="4" :push="3">
            <div class="pwdcheck-lbl" align="center">
              <h4 style="font-family:pt-sans-caption,sans-serif;font-weight:700;">Code:</h4>
            </div>
          </el-col>
          <el-col :span="6" :push="3">
            <div class="pwdcheck-ipt" style="margin-top: 15px;">
              <el-input class="pwdcheck" placeholder="请输入4位验证码" type="text" v-model="verifyInput"
                        size="medium" minlength="4" clearable required />
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
        <el-row :type="'flex'" :justify="'space-around'">
          <el-col :span="12" align="center">
            <div class="confirm-info">
              <el-button class="confirm-btn" type="warning" v-on:click="resetPwdCheckin" round>Reset</el-button>
            </div>
          </el-col>
          <el-col :span="12" align="center">
            <div class="cancel">
              <el-button class="cancel-btn" type="danger" @click="toHomePage" round>Go back</el-button>
            </div>
          </el-col>
        </el-row>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import SIdentify from './verifyCode'

export default {
  components: {
    's-identify': SIdentify
  },
  data () {
    return {
      usrName: localStorage.getItem('name'),
      passwd: localStorage.getItem('password'),
      username: '',
      pwdNew: '',
      verifyInput: '',
      identifyCode: '',
      identifyCodes: '1234567890'
    }
  },
  methods: {
    resetPwdCheckin: function () {
      if (this.username !== this.usrName) {
        this.$alert('用户名错误！', '修改失败', {
          confirmButtonText: '确定',
          callback: action => {
            this.$message({
              type: 'error',
              message: '请重新输入用户名'
            })
          },
          showClose: false
        })
      } else if (this.verifyInput !== this.identifyCode) {
        this.$alert('您输入的验证码有误！', '修改失败', {
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
        localStorage.setItem('password', this.pwdNew)
        this.$router.push({path: '/login'})
      }
    },
    pwdState: function (data) {
      this.visible = !(data === 'show')
    },
    toHomePage: function () {
      this.$router.push({path: '/'})
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
    }
  },
  created () {

  },
  mounted () {
    // 验证码初始化
    this.identifyCode = ''
    this.makeCode(4)
  }
}
</script>

<style scoped>
#forget-pwd{
  max-width: 800px;
  margin: 0 auto;
}
</style>
