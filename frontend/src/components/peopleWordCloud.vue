<template>
  <div id="people-wordcloud">
    <el-container>
        <main-header></main-header>
      <el-main>
        <el-row>
          <el-col>
            <div class="yearSelected">
              <el-select v-model="yearSelected" placeholder="请选择一个年份">
                <el-option
                  v-for="item in years"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col>
            <el-button @click="drawCloud" round class="button">画图</el-button>
          </el-col>
        </el-row>
        <div id="WordCloud"
             style="width: 800px;height: 400px;margin-top: 30px;margin-left: auto;margin-right:auto"></div>
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
        name: 'peopleWordCloud',
        components: {
            'main-header': MainHeader
        },
        data() {
            return {
                yearSelected: '',
                sname: '',
                serverResponse: '',
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
            }
        },
        mounted() {
        },
        //获取/choiceClouds传来的参数并存到sname里
        created() {
            let self = this
            self.getParams()
        },
        watch: {
            '$route': 'getParams'
        },
        methods: {
            getParams() {
                this.sname = this.$route.query.sname;
                // console.log(this.sname);
            },
            drawCloud: function () {
                var wordCloud = this.$echarts.init(document.getElementById('WordCloud'))
                // 先清空图例
                wordCloud.setOption({}, true)
                var that = this;
                const path = 'wordcnt/speaker?sname=' + this.sname + '&year=' + this.yearSelected;
                // const path = 'wordcnt/speaker?sname=' + this.sname + '&year=' + this.yearSelected;
                // const path = 'wordcnt/speaker?sname=Donald Trump&year=2015';
                //const path = 'wordcnt/speaker?sname=Donald Trump';
                this.axios.get(path).then(function (response) {
                    // console.log(response);
                    if (response.data.code == 2) {
                        that.$message.error('Request failed!');
                    } else if (response.data.code == 1) {
                        that.$message({
                            message: 'Empty data!',
                            center: true
                        })
                    } else if (response.data.code == 0) {
                        var d = response.data.data;
                        var option = {
                            title: {
                                text: "WordCloud by Speaker"
                            },
                            tooltip: {},
                            series: [{
                                type: 'wordCloud',
                                // gridSize: 20,
                                gridSize: 35,
                                // sizeRange: [12, 50],
                                sizeRange: [25, 75],
                                rotationRange: [0, 0],
                                shape: 'circle',
                                textStyle: {
                                    normal: {
                                        fontWeight: 'bold',
                                        color: function () {
                                            var colors = ['#60acfc', '#39B3EA', '#32d3eb', '#41CEC7', '#5bc49f', '#D4EC58', '#feb64d', '#FA816D', '#ff7c7c', '#D660A8', '#9287e7', '#668ED7'];
                                            return colors[parseInt(0.5 * Math.random() * 10 + 0.5 * Math.random() * 10)];
                                            // return 'rgb(' + [
                                            //     Math.round(Math.random() * 160),
                                            //     Math.round(Math.random() * 160),
                                            //     Math.round(Math.random() * 160)
                                            // ].join(',') + ')';
                                        }
                                    },
                                    emphasis: {
                                        shadowBlur: 10,
                                        // shadowColor: '#333'#f1f2f6
                                        shadowColor: '#a4b0be'
                                    }
                                },
                                data: d
                            }]
                        }
                        wordCloud.setOption(option);
                    }
                });
            }
        }
    }
</script>

<style scoped>
  .el-button {
    margin-right: 200px;
  }

  .el-select {
    width: 220px;
  }

  .el-col {
    width: 250px;
  }

  .el-row {
    padding-top: 30px;
    margin-left: 140px;
  }

  .el-main {
    margin: auto;
  }

</style>
