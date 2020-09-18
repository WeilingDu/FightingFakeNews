<template>
  <div id="news-detect">
    <el-container>
      <main-header></main-header>
      <el-main>
        <el-button type="primary" @click="download">下载数据</el-button>
        <el-row justify="center" type="flex">
          <el-col :span="12">
            <el-input v-model="keyword" placeholder="请输入任何你想搜索的新闻" size="medium"
                      @change="search">
              <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
            </el-input>
          </el-col>
        </el-row>
        <!--        展示搜索结果-->
        <div v-show="showSearchRes">
          <!--          展示新闻-->
          <div id="newsList" class="newsList">
            <h1>新闻</h1>
            <span v-show="news.length === 0">没有关于 {{keyword}} 的新闻</span>

            <ul v-for="item in news">
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
                  <el-button type="primary" plain @click="getAnalysis(item.id)">查看更多</el-button>
                </div>
              </el-card>
            </ul>
          </div>
          <!--        展示 speaker-->
          <div>
            <h1>人物</h1>
            <span v-show="speaker.length === 0">没有关于 {{keyword}} 的新闻</span>
            <ul v-for="item in speaker">

              <el-card shadow="hover">
                <div>
                  <span>
                    <i class="el-icon-user-solid"></i>
                    {{item.name}}
                  </span>
                  <el-divider></el-divider>
                  <el-button type="primary" plain @click="speakerInfo(item.name)">查看更多</el-button>
                </div>
              </el-card>
            </ul>
          </div>
          <!--        展示 party-->
          <div>
            <h1>党派</h1>
            <span v-show="party.length=== 0">没有关于 {{keyword}} 的新闻</span>

            <ul v-for="item in party">
              <el-card shadow="hover">
                <div>
                  <span>
                    <i class="el-icon-s-flag"></i>
                    {{item.name}}
                  </span>
                  <el-divider></el-divider>
                  <el-button type="primary" plain @click="partyInfo(item.name)">查看更多</el-button>
                </div>
              </el-card>
            </ul>
          </div>
        </div>
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
        name: 'NewsDetect',
        components: {
            'main-header': MainHeader
        },
        data() {
            return {
                showSearchRes: false,
                keyword: "",
                speaker: [],
                news: [],
                party: []
            }
        },
        mounted() {
        },
        methods: {
            search() {
                if (this.keyword.length === 0) {
                    this.speaker = [];
                    this.party = [];
                    this.news = [];
                    return;
                }
                this.speaker = [];
                this.party = [];
                this.news = [];
                const path = "search?keyword=" + this.keyword;
                let _t = this;
                this.axios.get(path).then(function (response) {
                    if (response.data.code === 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code === 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code === 0) {
                        _t.speaker = response.data.data.speaker;
                        _t.news = response.data.data.news;
                        _t.party = response.data.data.party;
                        _t.showSearchRes = true;
                    }
                })
            },
            speakerInfo(name) {
                this.$router.push({path: "/speaker", query: {sname: name}});
            },
            download() {
                window.location.href = "http://localhost:5000/data/download";

                // const path = "data/download";
                //
                // let _t = this;
                // this.axios.get(path).then(function (response) {
                //     alert("data");
                //     // console.log(response.data.code);
                //     if (response.data.code == 2) {
                //         _t.$message.error('Request failed!');
                //     } else if (response.data.code == 1) {
                //         _t.$message.error('Empty data!');
                //     } else if (response.data.code == 0) {
                //         _t.checkList = []; //清空已选
                //         _t.total = Math.ceil(parseInt(response.data.data["length"]) / _t.pagesize);
                //         _t.items = response.data.data["res"];
                //     }
                // })
            },
            partyInfo(name) {
                this.$router.push({path: "/party", query: {pname: name}});
            },
            handleClick(tab, event) {
                console.log(tab, event);
            },
            searchSpeaker() {

            },

            initPage1: function () {

                const path = 'news?mode=1&wd=' + this.value1 + '&page=' + this.currentpage + '&num=' + this.pagesize;

                let _t = this;
                this.axios.get(path).then(function (response) {
                    // console.log(response.data.code);
                    if (response.data.code == 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code == 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code == 0) {
                        _t.checkList = []; //清空已选
                        _t.total = Math.ceil(parseInt(response.data.data["length"]) / _t.pagesize);
                        _t.items = response.data.data["res"];
                    }
                })
            },
            initPage2: function () {

                const path = 'news?mode=2&wd=' + this.value2 + '&page=' + this.currentpage + '&num=' + this.pagesize;

                let _t = this;
                this.axios.get(path).then(function (response) {
                    // console.log(response.data.code);
                    if (response.data.code == 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code == 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code == 0) {
                        _t.checkList = []; //清空已选
                        _t.total = Math.ceil(parseInt(response.data.data["length"]) / _t.pagesize);
                        _t.items = response.data.data["res"];
                    }
                })
            },
            initPage3: function () {

                const path = 'news?mode=3&wd=' + this.text + '&page=' + this.currentpage + '&num=' + this.pagesize;

                let _t = this;
                this.axios.get(path).then(function (response) {
                    // console.log(response.data.code);
                    if (response.data.code == 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code == 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code == 0) {
                        _t.checkList = []; //清空已选
                        _t.total = Math.ceil(parseInt(response.data.data["length"]) / _t.pagesize);
                        _t.items = response.data.data["res"];
                    }
                })
            },
            //分页相关
            handleSizeChange(val) {
                let thispage = this;
                thispage.pagesize = val;
                thispage.currentpage = 1;
                thispage.initPage();

            },
            handleCurrentChange(val) {
                let thispage = this;
                thispage.currentpage = val;
                thispage.initPage();
            },
            // 跳转/newsAnalysis并传参
            getAnalysis: function (id) {
                this.$router.push({path: "/newsAnalysis", query: {news_id: id}});
            }
        }
    }
</script>

<style scoped>
  #speaker {
    width: 200px;
    display: inline-block;
    font-family: pt-sans, sans-serif;
    font-weight: 400;
  }

  #party {
    width: 200px;
    display: inline-block;
    font-family: pt-sans, sans-serif;
    font-weight: 400;
  }

  #statement {
    width: 550px;
    display: inline-block;
    font-family: pt-sans, sans-serif;
    font-style: italic;
    font-weight: 400;
  }


</style>
