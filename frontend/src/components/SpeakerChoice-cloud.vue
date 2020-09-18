<template>
  <div id="speaker-choice-cloud">
    <el-container>
        <main-header></main-header>
      <el-main>
        <div>
          <el-row justify="center">
            <el-col :span="12" :offset="4">
              <el-form >
                <el-form-item label="选择人物名字首字母">
                  <div>
                    <el-select
                      v-model="selected"
                      placeholder="请选择"
                      @change="showSpeakersFromIndex"
                    >
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
            <el-col :span="6">
              <el-button
                @click="showAll=!showAll;showIndexedSpeaker=false"
                type="primary"
              >查看 / 隐藏所有人物
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div v-show="showIndexedSpeaker">
          <div v-for="s in indexedSpeakers" style="margin:5px">
            <el-button id="speaker1" type="success" round @click="details(s)">{{s}}</el-button>
          </div>
        </div>
        <div id="speakerlist" v-show="showAll">
          <div v-for="name in this.speakers">
            <div>
              <center>
                <h1 style="color:#2E86C1">{{name[0]}}</h1>
              </center>
            </div>
            <div v-for="s in name[1]" style="margin:5px;">
              <el-button id="speaker2" type="success" round @click="details(s)">{{s}}</el-button>
            </div>
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
  import MainHeader from "./MainHeader";

  export default {
    name: "SpeakerChoiceCloud",
    data() {
      return {
        speakers: [],
        speakersSet: [],
        selected: "A",
        indexs: [],
        indexedSpeakers: [],
        showAll: false,
        showIndexedSpeaker: true,
        state1: ""
      };
    },
    components: {
      "main-header": MainHeader
    },
    mounted() {
      this.getName();
    },
    methods: {
      showSpeakersFromIndex: function () {
        this.indexedSpeakers = this.speakers[this.selected][1];
        this.showIndexedSpeaker = true;
      },
      getSpeakersSet() {
        let d = [];
        // console.log(this.speakers);
        for (let i = 0; i < this.speakers.length; i++) {
          let k = this.speakers[i][1];
          d = d.concat(k);

        }
        this.speakersSet = d;
        // console.log(d);

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
      //跳转/peopleWordCloud并传参
      details: function (name) {
        this.$router.push({path: "/peopleWordCloud", query: {sname: name}});
      }
    }
  };
</script>

<style scoped>
  .el-row{
    padding-top: 20px;
  }
  #speaker1{
    margin-left: 340px;
  }
  #speaker2{
    margin-left: 340px;
  }
</style>
