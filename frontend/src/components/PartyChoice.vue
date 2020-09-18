<template>
  <div id="party-choice">
    <el-container>
      <main-header></main-header>
      <el-main>
        <div>
          <el-row justify="center" type="flex">
            <el-col :span="6" >
              <el-form>
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
                @click="setShowAll"
                type="primary">
                查看 / 隐藏所有党派
              </el-button>
            </el-col>
          </el-row>
           <el-row>
            <el-col :span="5" :offset="17">
              总共 <span style="color: #2E86C1;font-weight: bolder">{{partyCnt}}</span> 个党派在录
            </el-col>
          </el-row>
        </div>
        <div v-show="showIndexedParty">
          <div v-for="s in indexedParties" class="p">
            <el-button @click="details(s)" type="success" round class="item">{{s}}</el-button>
          </div>
        </div>
        <div id="partylist" v-show="showAll">
          <div v-for="name in this.parties" class="p">
            <div>
              <div v-for="s in name[1]">
                <el-button @click="details(s)" type="success" round class="item">{{s}}</el-button>
              </div>
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
<style>
  body{
    margin: 0 0 0 0;
  }
</style>
<script>
    import MainHeader from "./MainHeader";

    export default {
        name: "PartyChoice",
        data() {
            return {
                parties: [],
                partiesSet: [],
                selected: "A",
                indexs: [],
                indexedParties: [],
                showAll: false,
                showIndexedParty: true,
                state1: "",
                partyCnt:0,
            };
        },
        components: {
            "main-header": MainHeader
        },
        mounted() {
            this.getName();
            this.getPartyCnt();

        },
        methods: {
            setShowAll: function () {
                this.showAll = !this.showAll;
                this.showIndexedParty = false
            },
            showPartiesFromIndex: function () {
                this.indexedParties = this.parties[this.selected][1];
                this.showIndexedParty = true;
                this.showAll = false;
            },
            getPartiesSet() {
                let d = [];
                for (let i = 0; i < this.partiesSet.length; i++) {
                    let k = this.parties[i][1];
                    d = d.concat(k);
                }
                this.partiesSet = d;
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
            getPartyCnt: function () {
                let _t = this;
                this.axios.get("party/cnt").then(function (response) {
                    _t.partyCnt = response.data.data['cnt'];
                });

            },
            //跳转/party并传参
            details: function (name) {
                this.$router.push({path: "/party", query: {pname: name}});
            }
        }
    };
</script>

<style scoped>
  .item {
    display: block;
    float: left;
    font-size: 18px;
    text-align: center;
    margin: 10px 10px 10px 0;
    overflow: hidden;
  }

  .p {
    text-align: center;
    margin-top: 2px;
    overflow: auto;
    margin-left: 200px
  }
</style>
