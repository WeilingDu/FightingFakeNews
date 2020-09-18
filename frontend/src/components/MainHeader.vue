<template >
    <el-menu mode="horizontal"
             router
             text-color="#fff"
             active-text-color="#FF7E00"
             background-color="#25292d">
      <el-row type="flex" justify="center">
        <el-col :offset="1">
          <img src="../assets/Fighting-Fake-News-blue.jpg" alt="" width="80px" height="50px">
        </el-col>
        <el-col>
          <el-menu-item index="/" class="menu-item">主页</el-menu-item>
        </el-col>
        <el-col>
          <el-submenu index="1" class="menu-item">
            <template slot="title" class="menu-item">数据统计</template>
            <el-menu-item index="/year">按年度</el-menu-item>
            <el-menu-item index="/location">按地点</el-menu-item>
          </el-submenu>
        </el-col>
        <el-col>
          <el-submenu index="2">
            <template slot="title" class="menu-item">数据可视化</template>
            <el-menu-item index="/speakerChoice">人物数据可视化</el-menu-item>
            <el-menu-item index="/partyChoice">党派数据可视化</el-menu-item>
            <el-menu-item index="/yearWordCloud">年度词云</el-menu-item>
            <el-menu-item index="/choiceClouds">人物词云</el-menu-item>
            <el-menu-item index="/choiceCloudp">党派词云</el-menu-item>
            <el-menu-item index="/vis/horizontal">横向比较</el-menu-item>
          </el-submenu>
        </el-col>
        <el-col>
          <el-menu-item index="/modelComparison" class="menu-item">机器学习模型分析</el-menu-item>
        </el-col>
        <el-col>
          <el-menu-item index="/newsPresent" class="menu-item">新闻中心</el-menu-item>
        </el-col>
        <el-col>
          <el-menu-item index="/searchCenter" class="menu-item">搜索中心</el-menu-item>
        </el-col>
        <el-col>
          <el-submenu index="4" class="menu-item">
            <template slot="title" >用户管理</template>
            <el-menu-item index="/login">登录</el-menu-item>
            <el-menu-item index="/reset">修改密码</el-menu-item>
            <el-menu-item index="/" @click="logout">退出</el-menu-item>
          </el-submenu>
        </el-col>
        <el-col :offset="1">

        </el-col>
      </el-row>
    </el-menu>
</template>

<script>
    export default {
        name: 'MainHeader',
        data() {
            return {
                activeIndex: '1'
            }
        },
        methods: {
            logout:function () {
                let storage=window.localStorage;
                storage.removeItem("token");
                this.$message(
              {
                type: 'success', message: 'Success Logout!'
              });
                window.location.href = "/";
            }
        }
    }
    document.querySelector('html').style.fontSize = '100'

</script>

<style scoped>
  .menu-item{
    font-size: 18px;
    margin: 0 0 0 0;
  }

</style>
