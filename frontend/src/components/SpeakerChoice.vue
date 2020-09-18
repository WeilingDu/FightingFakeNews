<template>
  <div id="speaker-choice">
    <el-container>
      <main-header></main-header>
      <el-main>
        <div>
          <el-row justify="center" type="flex">
            <el-col :span="6" :offset="1">
              <el-form>
                <el-form-item label="选择人物名字首字母">
                  <div>
                    <el-select
                      v-model="selected"
                      placeholder="请选择"
                      @change="showSpeakersFromIndex">
                      <el-option
                        v-for="item in indexs"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                      ></el-option>
                    </el-select>
                  </div>
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="4">
              <el-button
                @click="setShowAllSpeakers"
                type="primary">
                查看 / 隐藏所有人物
              </el-button>
            </el-col>
            <el-col :span="4">
              <el-button
                @click="setDirectlySearch"
                type="primary">
                按关键词直接搜索
              </el-button>
            </el-col>

          </el-row>
          <el-row>
            <el-col :span="5" :offset="17">
              总共 <span style="color: #2E86C1;font-weight: bolder">{{speakerCnt}}</span> 位人物在录
            </el-col>
          </el-row>
        </div>
        <div v-show="showIndexedSpeaker" style="text-align: center;margin-top: 10px;overflow: auto;margin-left: 100px">
          <div v-for="s in indexedSpeakers">
            <div>
              <div class="item">
                <a @click="details(s)">
                  <img src="../../static/t.png" alt="a"/>
                  <p>{{s}}</p>
                </a>
              </div>
            </div>
          </div>
        </div>
        <div v-show="showAll">
          <div v-for="name in this.speakers">
            <div style="text-align: center;">
              <h1>{{name[0]}}</h1>
            </div>
            <div style="text-align: center;margin-top: 10px;overflow: auto;margin-left: 100px">
              <div v-for="s in name[1]">
                <div class="item">
                  <a @click="details(s)">
                    <img src="../../static/t.png" alt="a"/>
                    <p>{{s}}</p>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--        检索-->
        <el-row v-show="directlySearch">
          <el-input v-model="query" placeholder="plz input speaker name"></el-input>
          <div style="text-align: center;margin-top: 10px;overflow: auto;margin-left: 100px">
            <div v-for="s in this.searchResults">
              <div class="item">
                <a @click="details(s.name)">
                  <img src="../../static/t.png" alt="a"/>
                  <p>{{s.name}}</p>
                </a>
              </div>
            </div>
          </div>
        </el-row>
      </el-main>
      <el-footer>
        <p style="color: gainsboro;text-align: center">Copyright &copy; 2019 HITSZ</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
    import MainHeader from "./MainHeader";

    export default {
        name: "SpeakerChoice",
        data() {
            return {
                speakers: [],
                speakersSet: [],
                searchResults: [],
                selected: "A",
                indexs: [],
                indexedSpeakers: [],
                showAll: false,
                showIndexedSpeaker: true,
                state1: "",
                query: "",
                directlySearch: false,
                speakerCnt:0
            };
        },
        components: {
            "main-header": MainHeader
        },
        mounted() {
            this.getName();
        },
        watch: {
            query: function (o, n) {
                if (this.query.length === 0) {
                    this.tableData = [];
                    return
                }
                let _t = this;
                this.axios
                    .get('search/speaker?query=' + this.query)
                    .then(function (response) {
                        _t.searchResults = response.data.data;
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        },
        methods: {
            setDirectlySearch: function () {
                this.directlySearch = true;
                this.showAll = false;
                this.showIndexedSpeaker = false;
            },
            setShowAllSpeakers: function () {
                this.directlySearch = false;
                this.showAll = !this.showAll;
                this.showIndexedSpeaker = false;
            },
            showSpeakersFromIndex: function () {
                this.indexedSpeakers = this.speakers[this.selected][1];
                this.showIndexedSpeaker = true;
                this.showAll = false;
                this.directlySearch = false;
            },
            getSpeakersSet() {
                let d = [];
                // console.log(this.speakers);
                for (let i = 0; i < this.speakers.length; i++) {
                    let k = this.speakers[i][1];
                    d = d.concat(k);

                }
                this.speakersSet = d;
                this.speakerCnt = this.speakersSet.length;


            },
            getName: function () {
                let _t = this;
                this.axios.get("speakers").then(function (response) {
                    _t.speakers = response.data;
                    _t.indexs = _t.speakers.map((x, i) => {
                        return {value: i, label: x[0]};
                    });

                    _t.getSpeakersSet();
                });

            },
            //跳转/speaker并传参
            details: function (name) {
                this.$router.push({path: "/speaker", query: {sname: name}});
            }
        }
    };
</script>

<style scoped>
  .el-row {
    padding-top: 20px;
  }

  #speaker1 {
    margin-left: 340px;
  }

  #speaker2 {
    margin-left: 340px;
  }

  .view-info {
    margin: auto;
    box-sizing: content-box;
    width: 70%;
    height: 580px;
    overflow: hidden;
    /*box-shadow: 2px 4px 6px #57606f;*/
  }

  .indexedItem {
    padding-top: 3%;
  }

  .item {
    display: block;
    float: left;
    color: sandybrown;
    font-size: 18px;
    text-align: center;
    margin: 10px 10px 10px 0;
    width: 200px;
    height: 200px;
    overflow: hidden;
  }

  img {
    width: 60%;
    height: 60%;
  }
</style>
