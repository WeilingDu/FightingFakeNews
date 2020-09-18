<template>
  <div id="speaker-analyse">
    <main-header></main-header>
    <div class="c">
      <el-row type="flex" justify="center">
        <el-col>
          <h1>{{sname}}</h1>
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <el-tabs v-model="activeName" @tab-click="click">
            <el-tab-pane label="基本信息" name="basic">
              <h2>党派: {{info['party']}}</h2>
              <h2>家乡: {{info['stateInfo']}}</h2>
            </el-tab-pane>
            <el-tab-pane label="历史信用" name="ch">
              <div
                id="ch"
                style="width: 1000px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"
              ></div>
            </el-tab-pane>
            <el-tab-pane label="词云" name="cloud">
              <div
                id="cloud"
                style="width: 1000px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"
              ></div>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import MainHeader from "./MainHeader";

export default {
  name: "SpeakerAnalyse",
  data() {
    return {
      activeName: "ch",
      sname: "",
      ch: [],
      info: [],
      cloud: []
    };
  },
  components: {
    "main-header": MainHeader
  },
  created() {
    this.getParams();
    this.getInfoByName();
    this.getChByName();
    this.getCloudByName();
  },
  methods: {
    getInfoByName() {
      var _t = this;
      this.axios
        .get("/speaker/info", { params: { sname: _t.sname } })
        .then(function(res) {
          // console.log(_t.sname);
          // console.log(res.data.data['party']);
          _t.info = res.data.data;
        });
    },
    getChByName: function() {
      var _t = this;
      this.axios
        .get("ch/speaker", { params: { sname: _t.sname } })
        .then(function(res) {
          if(res.data.code == 2){
            _t.$message.error('Request failed!');
          }
          else if (res.data.code == 1) {
            that.$message({
            message: 'Empty data!',
            center: true
            })
          }
          else if (res.data.code == 0) {
            _t.ch = res.data.data;
            _t.drawCh();
          }
        });
    },
    getCloudByName() {
      var _t = this;
      this.axios
        .get("wordcnt/speaker", { params: { sname: _t.sname , year:0} })
        .then(function(res) {
          if (res.data.code === 0) {
            _t.cloud = res.data.data;
          } else {
            alert("no related data from cloud");
          }
        });
    },
    getParams() {
      this.sname = this.$route.query.sname;
    },
    drawCh() {
      var d = new Array();
      for (var k in this.ch) {
        // console.log(d);
        if(k === 'FalseCounts'){
          d.push({ name: 'False', value: this.ch[k] });
        }else if (k === 'TrueCounts') {
          d.push({ name: 'True', value: this.ch[k] });
        }else if (k === 'halfTrueCounts') {
          d.push({ name: 'Half True', value: this.ch[k] });
        }else if (k === 'mostlyFalseCounts') {
          d.push({ name: 'Mostly False', value: this.ch[k] });
        }else if (k === 'mostlyTrueCounts') {
          d.push({ name: 'Mostly True', value: this.ch[k] });
        }else {
          d.push({ name: 'On Fire', value: this.ch[k] });
        }
      }
      // console.log(d);
      var r = this.$echarts.init(document.getElementById("ch"));
      r.clear();
      var option = {
        color: ['#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c', '#9287e7'],
        title: {
          text: "Credit History of " + this.sname,
          // subtext: "xxx",
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          type: "scroll",
          orient: "vertical",
          right: 10,
          top: 20,
          bottom: 20,
          data: [
            "True",
            "Mostly True",
            "Half True",
            "Mostly False",
            "False",
            "On Fire"
          ]
        },
        series: [
          {
            name: this.sname,
            type: "pie",
            radius: "55%",
            center: ["40%", "50%"],
            data: d,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowfOfsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      r.setOption(option);
    },
    drawCloud() {
      var wordCloud = this.$echarts.init(document.getElementById("cloud"));
      var d = this.cloud;
      var option = {
        title: {
          text: "Word Cloud of " + this.sname,
        },
        tooltip: {},
        series: [
          {
            type: "wordCloud",
            gridSize: 10,
            sizeRange: [25, 75],
            rotationRange: [0, 0],
            shape: "circle",
            textStyle: {
              normal: {
                color: function() {
                  var colors = ['#60acfc', '#39B3EA', '#32d3eb', '#41CEC7', '#5bc49f', '#D4EC58', '#feb64d', '#FA816D', '#ff7c7c', '#D660A8', '#9287e7', '#668ED7'];
                  return colors[parseInt(0.5 * Math.random() * 10 + 0.5 * Math.random() * 10)];
                }
              },
              emphasis: {
                shadowBlur: 10,
                  shadowColor: '#a4b0be'
              }
            },
            data: d
          }
        ]
      };
      wordCloud.setOption(option);
    },
    click: function(tab, event) {
      if (this.activeName == "basic") {
      } else if (this.activeName === "ch") {
        this.drawCh();
      } else if (this.activeName === "cloud") {
        this.drawCloud();
      }
    },

    tabChange: function() {
      if (this.activeName == "basic") {
      } else if (this.activeName === "ch") {
        this.drawCh();
      } else if (this.activeName === "cloud") {
      }
    }
  }
};
</script>

<style scoped>
.c {
  margin-top: 10px;
  margin-left: 200px;
  margin-right: 200px;
}
</style>
