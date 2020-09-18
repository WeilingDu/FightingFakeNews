<template>
  <div id="TorF-analyse-location">
    <el-container>

        <main-header></main-header>
      <el-main>
      </el-main>
      <el-footer>
        <p style="color: gainsboro;text-align: center">Copyright &copy; 2019 HITSZ</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import MainHeader from './MainHeader'

export default {
  name: 'TFAnalyse-location',
  components:{
    'main-header':MainHeader
  },
  data () {
    return {
    }
  }
}
</script>

<style scoped>

</style>
