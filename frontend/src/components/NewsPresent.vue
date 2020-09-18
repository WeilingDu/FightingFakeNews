<template>
  <div id="news-detect">
    <el-container>
        <main-header></main-header>
      <el-main>
        <el-tabs v-model="activeName" @tab-click="handleClick" style="font-family:pt-sans-caption,sans-serif;font-weight:400;">
          <el-tab-pane label="人物" name="first">
            <el-select v-model="value1" placeholder="请选择人物名字首字母">
              <el-option
                v-for="item in options1"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-button type="primary" id="search1" icon="el-icon-search" @click="initPage1">搜索</el-button>
          </el-tab-pane>
          <el-tab-pane label="党派" name="second" style="font-family:pt-sans-caption,sans-serif;font-weight:400;">
            <el-select v-model="value2" placeholder="请选择党派名字首字母">
              <el-option
                v-for="item in options2"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-button type="primary" id="search2" icon="el-icon-search" @click="initPage2">搜索</el-button>
          </el-tab-pane>
          <el-tab-pane label="言论" name="third" style="font-family:pt-sans-caption,sans-serif;font-weight:400;">
            <el-input
              style="width: 300px"
              type="text"
              size="large"
              placeholder="请输入... "
              v-model="text"
              maxlength="30"
              show-word-limit
            >
            </el-input>
            <el-button type="primary" id="search3" icon="el-icon-search" @click="initPage3">搜索</el-button>
          </el-tab-pane>
        </el-tabs>
        <div id="newsList" class="newsList">
          <!--<ul>-->
            <ul v-for="item in items">
              <el-card shadow="hover">
                <div>
                  <span id="speaker">
                    <i class="el-icon-user-solid"></i>
                    {{item.speaker}}
                  </span>
                  <span id="party">
                    <i class="el-icon-s-flag"></i>
                    {{item.party}}
                  </span>
                  <el-divider></el-divider>
                  <span id="statement">
                    <i class="el-icon-document"></i>
                    {{item.statement}}
                  </span>
                  <el-button type="primary" plain @click="getAnalysis(item.id)">Details</el-button>
                </div>
              </el-card>
            </ul>
          <!--</ul>-->
        </div>
        <div id="pager" class="pager01">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentpage"
            :page-sizes="pageSizesList"
            :page-size="pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
          </el-pagination>
        </div>
      </el-main>
      <el-footer>
        <p style="color: gainsboro;text-align: center">Copyright &copy; 2019 HITSZ</p>
      </el-footer>
    </el-container>
  </div>
</template>
<style>
  body{
    margin: 0 0 0 0;
  }
</style>
<script>
  import MainHeader from './MainHeader'

  export default {
    name: 'NewsDetect',
    components: {
      'main-header': MainHeader
    },
    data () {
      return {
        activeName: 'second',
        items: [],
        pageSizesList: [10, 20, 30, 50],
        pagesize: 10,
        currentpage: 1,
        total: 0,
        // speaker
        options1: [
          {value: 'A', label: 'A'},
          {value: 'B', label: 'B'},
          {value: 'C', label: 'C'},
          {value: 'D', label: 'D'},
          {value: 'E', label: 'E'},
          {value: 'F', label: 'F'},
          {value: 'G', label: 'G'},
          {value: 'H', label: 'H'},
          {value: 'I', label: 'I'},
          {value: 'J', label: 'J'},
          {value: 'K', label: 'K'},
          {value: 'L', label: 'L'},
          {value: 'M', label: 'M'},
          {value: 'N', label: 'N'},
          {value: 'O', label: 'O'},
          {value: 'P', label: 'P'},
          {value: 'Q', label: 'Q'},
          {value: 'R', label: 'R'},
          {value: 'S', label: 'S'},
          {value: 'T', label: 'T'},
          {value: 'U', label: 'U'},
          {value: 'V', label: 'V'},
          {value: 'W', label: 'W'},
          {value: 'X', label: 'X'},
          {value: 'Y', label: 'Y'},
          {value: 'Z', label: 'Z'},
          ],
        value1: '',
        // party
        options2: [
          {value: 'A', label: 'A'},
          {value: 'B', label: 'B'},
          {value: 'C', label: 'C'},
          {value: 'D', label: 'D'},
          {value: 'E', label: 'E'},
          {value: 'F', label: 'F'},
          {value: 'G', label: 'G'},
          {value: 'H', label: 'H'},
          {value: 'I', label: 'I'},
          {value: 'J', label: 'J'},
          {value: 'K', label: 'K'},
          {value: 'L', label: 'L'},
          {value: 'M', label: 'M'},
          {value: 'N', label: 'N'},
          {value: 'O', label: 'O'},
          {value: 'P', label: 'P'},
          {value: 'Q', label: 'Q'},
          {value: 'R', label: 'R'},
          {value: 'S', label: 'S'},
          {value: 'T', label: 'T'},
          {value: 'U', label: 'U'},
          {value: 'V', label: 'V'},
          {value: 'W', label: 'W'},
          {value: 'X', label: 'X'},
          {value: 'Y', label: 'Y'},
          {value: 'Z', label: 'Z'},
        ],
        value2: '',
        // statement
        text: ''
      }
    },
    mounted() {
      // this.initPage();
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      searchSpeaker(){

      },
      //重新加载页面方法放在VUE内部，打开页面和每次增删改操作都调用一次
      //演示用 initPage
      // initPage: function () {
      //   let thispage = this;
      //   thispage.items = [
      //     {id: 1, speaker: 1, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 2, speaker: 2, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 3, speaker: 3, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 4, speaker: 4, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 5, speaker: 5, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 6, speaker: 6, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 7, speaker: 7, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 8, speaker: 8, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'},
      //     {id: 9, speaker: 9, jobtitle: '图片', party: 'VUE', statement: 'news', torf: 't'}
      //   ];
      //   thispage.total = 110;
      // },
      //实际应用中的 initPage
      //根据speaker首字母来展示新闻
      initPage1: function () {

        const path = 'news?mode=1&wd=' + this.value1 + '&page=' + this.currentpage + '&num=' + this.pagesize;

        let _t = this;
        this.axios.get(path).then(function(response){
          // console.log(response.data.code);
          if(response.data.code == 2){
            _t.$message.error('Request failed!');
          }
          else if (response.data.code == 1) {
            _t.$message.error('Empty data!');
          }
          else if (response.data.code == 0) {
            _t.checkList=[]; //清空已选
            _t.total = Math.ceil(parseInt(response.data.data["length"])/_t.pagesize);
            _t.items = response.data.data["res"];
          }
        })
      },
      initPage2: function () {

        const path = 'news?mode=2&wd=' + this.value2 + '&page=' + this.currentpage + '&num=' + this.pagesize;

        let _t = this;
        this.axios.get(path).then(function(response){
          // console.log(response.data.code);
          if(response.data.code == 2){
            _t.$message.error('Request failed!');
          }
          else if (response.data.code == 1) {
            _t.$message.error('Empty data!');
          }
          else if (response.data.code == 0) {
            _t.checkList=[]; //清空已选
            _t.total = Math.ceil(parseInt(response.data.data["length"])/_t.pagesize);
            _t.items = response.data.data["res"];
          }
        })
      },
      initPage3: function () {

        const path = 'news?mode=3&wd=' + this.text + '&page=' + this.currentpage + '&num=' + this.pagesize;

        let _t = this;
        this.axios.get(path).then(function(response){
          // console.log(response.data.code);
          if(response.data.code == 2){
            _t.$message.error('Request failed!');
          }
          else if (response.data.code == 1) {
            _t.$message.error('Empty data!');
          }
          else if (response.data.code == 0) {
            _t.checkList=[]; //清空已选
            _t.total = Math.ceil(parseInt(response.data.data["length"])/_t.pagesize);
            _t.items = response.data.data["res"];
          }
        })
      },
      //分页相关
      handleSizeChange(val) {
        let thispage = this;
        thispage.pagesize=val;
        thispage.currentpage=1;
        thispage.initPage();

      },
      handleCurrentChange(val) {
        let thispage = this;
        thispage.currentpage=val;
        thispage.initPage();
      },
      // 跳转/newsAnalysis并传参
      getAnalysis: function(id){
        this.$router.push({path: "/newsAnalysis", query: {news_id: id}});
      }
    }
  }
</script>

<style scoped>
  main{
    height: 2400px;
    width: 900px;
    margin: auto;
  }
  #speaker{
    width: 200px;
    display: inline-block;
    font-family:pt-sans,sans-serif;
    font-weight:400;
  }
  #party{
    width: 200px;
    display: inline-block;
    font-family:pt-sans,sans-serif;
    font-weight:400;
  }
  #statement{
    width: 550px;
    display: inline-block;
    font-family:pt-sans,sans-serif;
    font-style: italic;
    font-weight:400;
  }
  #search1{
    margin-left: 200px;
  }


</style>
