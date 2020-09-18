<template>
  <div id="news-analysis">
    <el-container>
      <main-header></main-header>
      <el-row type="flex" justify="center">
        <h1 style="color: #ff9f43; font-family: bungee, sans-serif; font-weight: 800; font-size: xx-large">详细新闻及报告</h1>
      </el-row>
      <el-main>
        <h1>言论</h1>
        <el-card shadow="hover">
          <h3>{{statement}}</h3>
        </el-card>
        <h1>预测</h1>
        <el-card shadow="hover">
          <h3>新闻标签: {{label}}</h3>
          <h3 v-for="p in prediction">{{p.model}}: {{p.pred}}</h3>
        </el-card>
        <h1>人物</h1>
        <el-card shadow="hover">
          <h3>{{speaker}}</h3>
          <h3>{{party}}</h3>
          <div
            id="CreditHistory"
            style="width: 800px;height: 400px;margin-top: 30px;margin-left: auto;margin-right:auto"
          ></div>
        </el-card>

        <h1>相似新闻</h1>
        <el-card id="sim" shadow="hover">
          <div v-for="s in sim">
            {{s.sc}}:{{s.statement}}
            <el-button type="primary" plain @click="getAnalysis(s.id)">查看更多</el-button>
            <el-divider></el-divider>
          </div>
        </el-card>
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
        name: 'NewsAnalysis',
        data() {
            return {
                news_id: '',
                statement: '',

                label: '',
                prediction: [],

                speaker: 'Obama',
                party: 'Dxxx',

                // true: '1',
                mostlyTrue: '',
                halfTrue: '',
                mostlyFalse: '',
                false: '',
                onFire: '',

                sim: [],

            }
        },
        components: {
            'main-header': MainHeader
        },
        //获取/newsPresent传来的参数并存到news_id里
        created() {
            this.getParams();
            this.getInfo();
            this.getSimi();
            this.predict();
        },
        watch: {
            '$route': 'getParams'
        },
        methods: {
            getAnalysis: function (id) {
                window.location.href = "/newsAnalysis?news_id=" + id;
            },
            getParams() {
                this.news_id = this.$route.query.news_id;
            },
            draw() {
                let r = this.$echarts.init(document.getElementById("CreditHistory"));
                r.showLoading();
                r.clear();
                let option = {
                    title: {
                        text: "Credit History of " + this.speaker,
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
                            'Mostly-True',
                            'Half-True',
                            'Barely-True',
                            'False',
                            'Pants-Fire'
                        ]
                    },
                    series: [
                        {
                            name: this.speaker,
                            type: "pie",
                            radius: "55%",
                            center: ["40%", "50%"],
                            data: [
                                {value: this.true, name: 'True'},
                                {value: this.mostlyTrue, name: 'Mostly-True'},
                                {value: this.halfTrue, name: 'Half-True'},
                                {value: this.mostlyFalse, name: 'Barely-True'},
                                {value: this.false, name: 'False'},
                                {value: this.onFire, name: 'Pants-Fire'}
                            ],
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
                // console.log(option['series'][0]['data']);
                r.hideLoading();
                r.setOption(option);
            },
            getInfo() {
                const path = 'new?id=' + this.news_id;
                // console.log(path);

                let _t = this;
                _t.statement = '';
                _t.label = '';
                _t.speaker = '';
                _t.party = '';
                _t.mostlyTrue = '';
                _t.halfTrue = '';
                _t.false = '';
                _t.mostlyFalse = '';
                _t.onFire = '';

                this.axios.get(path).then(function (response) {
                    // console.log(response.data)
                    if (response.data.code === 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code === 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code === 0) {
                        // console.log(response.data.data)
                        let d = response.data.data;
                        _t.statement = d['statement'];
                        _t.label = d['label'];
                        _t.speaker = d['speaker'];
                        _t.party = d['partyAffiliation'];
                        _t.mostlyTrue = d['mostlyTrue'];
                        _t.halfTrue = d['halfTrue'];
                        _t.mostlyFalse = d['barelyTrue'];
                        _t.false = d['false'];
                        _t.onFire = d['pantsOnFire'];
                        _t.true = d["true"];

                        //画图
                        _t.draw();
                    }
                })
            },
            getSimi() {
                let _t = this;
                _t.sim = [];
                const path = 'sim?id=' + this.news_id;
                this.axios.get(path).then(function (response) {
                    if (response.data.code === 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code === 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code === 0) {
                        _t.sim = response.data.data;
                    }
                })
            },
            predict() {
                let _t = this;
                _t.predict_lr = '';
                const path = 'pred?id=' + this.news_id;
                this.axios.get(path).then(function (response) {
                    if (response.data.code === 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code === 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code === 0) {
                        _t.prediction = response.data.data;

                    }
                })
            },
        }
    }
</script>

<style scoped>
  /*main {*/
  /*  height: 2400px;*/
  /*  width: 900px;*/
  /*  margin: auto;*/
  /*}*/


</style>
