<template>
  <div id="party-choice-cloud">
    <el-container>
        <main-header></main-header>
      <el-main>
        <div>
          <el-row justify="center">
            <el-col :span="12" :offset="4">
              <el-form >
                <el-form-item label="选择党派名字首字母">
                  <div>
                    <el-select
                      v-model="selected"
                      placeholder="请选择"
                      @change="showPartiesFromIndex"
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
                @click="showAll=!showAll;showIndexedParty=false"
                type="primary"
              >查看 / 隐藏所有党派
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div v-show="showIndexedParty">
          <div v-for="s in indexedParties" style="margin:5px">
            <el-button id="party1" type="success" round @click="details(s)">{{s}}</el-button>
          </div>
        </div>
        <div id="partylist" v-show="showAll">
          <div v-for="name in this.parties">
            <div>
              <center>
                <h1 style="color:#2E86C1">{{name[0]}}</h1>
              </center>
            </div>
            <div v-for="s in name[1]" style="margin:5px;">
              <el-button id="party2" type="success" round @click="details(s)">{{s}}</el-button>
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
    name: "PartyChoiceCloud",
    data() {
      return {
        parties: [],
        partiesSet: [],
        selected: "A",
        indexs: [],
        indexedParties: [],
        showAll: false,
        showIndexedParty: true,
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
      showPartiesFromIndex: function () {
        this.indexedParties = this.parties[this.selected][1];
        this.showIndexedParty = true;
      },
      getPartiesSet() {
        let d = [];
        // console.log(this.parties);
        for (let i = 0; i < this.partiesSet.length; i++) {
          let k = this.parties[i][1];
          d = d.concat(k);

        }
        this.partiesSet = d;
        // console.log(d);

      },
      getName: function () {
        let _t = this;
        this.axios.get("party").then(function (response) {
          _t.parties = response.data;
          _t.indexs = _t.parties.map((x, i) => {
            return {value: i, label: x[0]};
          });
          _t.getPartiesSet();
        });

      },
      //跳转/partyWordCloud并传参
      details: function (name) {
        this.$router.push({path: "/partyWordCloud", query: {pname: name}});
      }
    }
  };
</script>

<style scoped>
  .el-row{
    padding-top: 20px;
  }
  #party1{
    margin-left: 340px;
  }
  #party2{
    margin-left: 340px;
  }
</style>
