<template>
  <div id="speaker-analyse">
    <el-container>

      <main-header></main-header>
      <el-main>
        <div class="c">
          <el-row type="flex" justify="center">
            <h1>横向比较</h1>
          </el-row>
          <el-row type="flex" justify="center" style="margin-bottom: 20px">
            <el-col>

              <el-select v-model="selected" placeholder="请选择">
                <el-option key="speaker" label="人物" value="speaker"></el-option>
                <el-option key="party" label="党派" value="party"></el-option>
              </el-select>
            </el-col>
            <el-col>
              <el-select v-model="year1" placeholder="起始年份">
                <el-option
                  v-for="item in years"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-col>
            <el-col>
              <el-select v-model="year2" placeholder="结束年份">
                <el-option
                  v-for="item in years"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-col>
          </el-row>
          <el-row type="flex" justify="center" v-if="selected === 'speaker'">
            <el-col :span="8">
              <el-select v-model="c1" filterable :filter-method="speakerFilter" placeholder="选择一位人物1">
                <el-option
                  v-for="item in speakers"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="8" :offset="1">
              <el-select v-model="c2" filterable :filter-method="speakerFilter" placeholder="选择一位人物2">
                <el-option
                  v-for="item in speakers"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-col>
          </el-row>
          <el-row type="flex" justify="center" v-if="selected === 'party'">
            <el-col :span="8">
              <el-select v-model="c1" filterable placeholder="选择一个党派1">
                <el-option
                  v-for="item in parties"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="8" :offset="1">
              <el-select v-model="c2" filterable placeholder="选择一个党派2">
                <el-option
                  v-for="item in parties"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-col>
          </el-row>
          <el-row justify="center" type="flex" style="margin-top: 20px">

            <el-button round type="primary" @click="drawHandler">画图</el-button>

          </el-row>

          <el-row>
            <el-col>
              <el-tabs v-model="activeName" @tab-click="click">
                <el-tab-pane label="数据统计" name="ch">
                  <div
                    id="ch1"
                    style="width: 1000px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"
                  ></div>
                  <div
                    id="ch2"
                    style="width: 1000px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"
                  ></div>
                </el-tab-pane>
                <el-tab-pane label="词云" name="cloud">
                  <div
                    id="cloud1"
                    style="width: 1000px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"
                  ></div>
                  <div
                    id="cloud2"
                    style="width: 1000px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"
                  ></div>
                </el-tab-pane>
              </el-tabs>
            </el-col>
          </el-row>
        </div>
      </el-main>
      <el-footer>
        <p style="color: gainsboro;text-align: center">Copyright &copy; 2019 HITSZ</p>
      </el-footer>
    </el-container>
  </div>

</template>
<style>
  body {
    margin: 0 0 0 0;
  }
</style>
<script>
    import MainHeader from "./MainHeader";

    export default {
        name: "SpeakerAnalyse",
        data() {
            return {
                activeName: "ch",
                selected: "",
                all_speakers: [],
                speakers: [],
                all_parties: [],
                parties: [],
                c1: "",
                c2: "",
                year1: 0,
                year2: 0,
                ch: {
                    "ch1": [],
                    "ch2": []
                },
                cloud: {
                    "cloud1": [],
                    "cloud2": []
                },
                info: [],
                years: [
                    {value: 0, label: '全部'},
                    {value: 2009, label: 2009},
                    {value: 2010, label: 2010},
                    {value: 2011, label: 2011},
                    {value: 2012, label: 2012},
                    {value: 2013, label: 2013},
                    {value: 2014, label: 2014},
                    {value: 2015, label: 2015},
                    {value: 2016, label: 2016},
                    {value: 2017, label: 2017},
                    {value: 2018, label: 2018},
                    {value: 2019, label: 2019},
                ],
            };
        },
        components: {
            "main-header": MainHeader
        },
        created() {
            this.getAllSpeakers();
            this.getAllParties();
        },
        methods: {
            speakerFilter: function (query) {
                if (query === "") {
                    this.speakers = this.all_speakers.slice(0, 50);
                    return;
                }
                let arr = this.all_speakers.filter((item) => {
                    return item.toLowerCase().includes(query.toLowerCase())
                });
                if (arr.length > 50) {
                    this.speakers = arr.slice(0, 50)
                } else {
                    this.speakers = arr
                }
            },
            getAllSpeakers: function () {
                let _t = this;
                this.axios
                    .get("/all_speakers")
                    .then(function (res) {
                        _t.all_speakers = res.data.data;
                        _t.speakerFilter()
                    });
            },
            getAllParties: function () {
                let _t = this;
                this.axios
                    .get("/all_parties")
                    .then(function (res) {
                        _t.parties = res.data.data;
                    });

            },
            getInfoByName() {
                let _t = this;
                this.axios
                    .get("/speaker/info", {params: {sname: _t.sname}})
                    .then(function (res) {
                        _t.info = res.data.data;
                    });
            },

            drawHandler: function () {
                this.drawChTwo();
                this.drawCloudTwo();
            },
            drawChTwo: function () {
                this.getChByName("ch1", this.c1);
                this.getChByName("ch2", this.c2);
            },
            drawCloudTwo: function () {
                this.getCloudByName("cloud1", this.c1);
                this.getCloudByName("cloud2", this.c2);
            },
            getChByName: function (ch, c) {
                let _t = this;
                let path = "";
                let param = {};
                if (this.selected === "speaker") {
                    path = "h/ch/speaker";
                    param = {speaker: c, year1: _t.year1, year2: _t.year2};
                } else if (this.selected === "party") {
                    path = "h/ch/party";
                    param = {party: c, year1: _t.year1, year2: _t.year2};
                }
                this.axios
                    .get(path, {params: param})
                    .then(function (res) {
                        if (res.data.code === 2) {
                            _t.$message.error('Request failed!');
                        } else if (res.data.code === 1) {
                            _t.$message({
                                message: 'Empty data!',
                                center: true
                            })
                        } else if (res.data.code === 0) {
                            _t.ch[ch] = res.data.data;
                            _t.drawCh(ch, c);
                        }
                    });
            },
            getCloudByName(cloud, c) {
                let _t = this;
                let path = "";
                let param = {};
                if (this.selected === "speaker") {
                    path = "h/wordcnt/speaker";
                    param = {speaker: c, year1: _t.year1, year2: _t.year2};
                } else if (this.selected === "party") {
                    path = "h/wordcnt/party";
                    param = {party: c, year1: _t.year1, year2: _t.year2};
                }
                this.axios
                    .get(path, {params: param})
                    .then(function (res) {
                        if (res.data.code === 0) {
                            // TODO:refactor this shit
                            _t.cloud[cloud] = res.data.data;
                            _t.drawCloud(cloud, c)
                        } else {
                            alert("no related data from cloud");
                        }
                    });
            },
            drawCh(ch, c) {
                let d = [];
                let currentCh = this.ch[ch];
                for (let k in currentCh) {
                    if (k === 'FalseCounts') {
                        d.push({name: 'False', value: currentCh[k]});
                    } else if (k === 'TrueCounts') {
                        d.push({name: 'True', value: currentCh[k]});
                    } else if (k === 'halfTrueCounts') {
                        d.push({name: 'Half True', value: currentCh[k]});
                    } else if (k === 'mostlyFalseCounts') {
                        d.push({name: 'Mostly False', value: currentCh[k]});
                    } else if (k === 'mostlyTrueCounts') {
                        d.push({name: 'Mostly True', value: currentCh[k]});
                    } else {
                        d.push({name: 'On Fire', value: currentCh[k]});
                    }
                }

                let r = this.$echarts.init(document.getElementById(ch));
                r.clear();
                let option = {
                    color: ['#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c', '#9287e7'],
                    title: {
                        text: "Credit History of " + c,
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
                                    shadowOffsetX: 0,
                                    shadowColor: "rgba(0, 0, 0, 0.5)"
                                }
                            }
                        }
                    ]
                };
                r.setOption(option);
            },
            drawCloud(cloud, c) {

                let wordCloud = this.$echarts.init(document.getElementById(cloud));
                let d = this.cloud[cloud];
                let option = {
                    title: {
                        text: "Word Cloud of " + c,
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
                                    color: function () {
                                        let colors = ['#60acfc', '#39B3EA', '#32d3eb', '#41CEC7', '#5bc49f', '#D4EC58', '#feb64d', '#FA816D', '#ff7c7c', '#D660A8', '#9287e7', '#668ED7'];
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
            click: function (tab, event) {
                if (this.activeName === "basic") {
                } else if (this.activeName === "ch") {
                    this.drawCh();
                } else if (this.activeName === "cloud") {
                    this.drawCloud();
                }
            },

            tabChange: function () {
                if (this.activeName === "basic") {
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
