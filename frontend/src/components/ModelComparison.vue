<template>
  <div id="model-comparison">
    <el-container>
      <main-header></main-header>
      <el-main>
        <el-row type="flex" justify="center">
          <h1 class="title">模型性能分析</h1>
        </el-row>
        <el-row type="flex" justify="center">
          <el-form>

            <el-radio-group v-model="featureSelected" size="medium">
              <el-tooltip effect="dark" content="Statement" placement="top">
                <el-radio-button label="1" key="1">1个特征</el-radio-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="Statement + Speaker" placement="top">
                <el-radio-button label="2" key="2">2个特征</el-radio-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="Statement + Speaker + Party" placement="top">
                <el-radio-button label="3" key="3">3个特征</el-radio-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="Statement + Speaker + Party + State" placement="top">
                <el-radio-button label="4" key="4">4个特征</el-radio-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="Statement + Speaker + Party + State + Credit History"
                          placement="top">
                <el-radio-button label="5" key="5">5个特征</el-radio-button>
              </el-tooltip>
            </el-radio-group>

          </el-form>
        </el-row>
        <el-row type="flex" justify="center" style="margin-top: 10px">
          <el-form>
            <el-radio-group v-model="chartSelected" size="medium">
              <el-radio-button label="1" key="1">折线图</el-radio-button>
              <el-radio-button label="2" key="2">柱状图</el-radio-button>
              <el-radio-button label="3" key="3">雷达图</el-radio-button>
            </el-radio-group>
            <el-button round @click="loadData">画图</el-button>
            <el-button type="primary" @click="train">训练模型</el-button>
          </el-form>
        </el-row>
        <div id="Graph"></div>
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
    import MainHeader from './MainHeader'

    export default {
        name: 'ModelComparison',
        components: {
            'main-header': MainHeader
        },
        data() {
            return {
                featureSelected: '',
                chartSelected: '',
                modelType: ['LR', 'RF'],
                performance: ['Accuracy', 'Precision', 'Recall', 'F1'],
                LR: [0.7, 0.5, 0.2, 0.8],
                RF: [0.1, 0.2, 0.9, 0.4],
                supportedModel: [],
                metrics: {},
                legend:[],
            }
        },
        mounted() {
            // this.loadData();
        },
        methods: {
            train: function () { // 用最新的数据重新训练模型
                this.$router.push({path:'/train'})
                // window.location.href = "/train";
            },
            draw: function (DrawChart) {
                if (this.chartSelected == 1) {
                    DrawChart.clear();
                    let option = {
                        color: ['#cd6f4e', '#2a4056'],
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'cross',
                                label: {
                                    backgroundColor: '#6a7985'
                                }
                            }
                        },
                        legend: {
                            data: this.legend
                        },
                        toolbox: {
                            feature: {
                                saveAsImage: {}
                            }
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: [
                            {
                                type: 'category',
                                boundaryGap: false,
                                data: this.performance
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value'
                            }
                        ],
                        series: this.generateSeries()
                    };
                    DrawChart.hideLoading();
                    DrawChart.setOption(option);
                } else if (this.chartSelected == 2) {
                    DrawChart.clear();
                    let option = {
                        color: ['#cd6f4e', '#2a4056'],
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow'
                            }
                        },
                        legend: {
                            data: this.legend
                        },
                        toolbox: {
                            show: true,
                            orient: 'vertical',
                            left: 'right',
                            top: 'center',
                            feature: {
                                saveAsImage: {show: true}
                            }
                        },
                        calculable: true,
                        xAxis: [
                            {
                                type: 'category',
                                axisTick: {show: false},
                                data: this.performance
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value'
                            }
                        ],
                        series: this.generateSeries()
                    };
                    DrawChart.hideLoading();
                    DrawChart.setOption(option);
                } else if (this.chartSelected == 3) {
                    DrawChart.clear();
                    let option = {
                        color: ['#cd6f4e', '#2a4056'],
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            x: 'center',
                            data: this.legend
                        },
                        radar: [
                            {
                                indicator: [
                                    {text: 'Accuracy', max: 1},
                                    {text: 'Precision', max: 1},
                                    {text: 'Recall', max: 1},
                                    {text: 'F1', max: 1}
                                ],
                                center: ['50%', '50%'],
                                radius: 150
                            }
                        ],
                        series: [
                            {
                                type: 'radar',
                                tooltip: {
                                    trigger: 'item'
                                },
                                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                                data: this.generateSeries()
                            }
                        ]
                    };
                    DrawChart.hideLoading();
                    DrawChart.setOption(option);
                } else {
                    this.$message.error('Please choose the chart type!');
                }
            },
            generateSeries: function () {
                let series = [];
                if (this.chartSelected == 1) {
                    for (let model in this.metrics) {
                        series.push({
                            name: model,
                            type: 'line',
                            stack: '总量',
                            areaStyle: {},
                            data: this.metrics[model]
                        })
                    }
                } else if (this.chartSelected == 2) {
                    for (let model in this.metrics) {
                        series.push({
                            name: model,
                            type: 'bar',
                            barGap: 0,
                            data: this.metrics[model]
                        })
                    }
                } else if (this.chartSelected == 3) {
                    for (let model in this.metrics) {
                        series.push({
                            value: this.metrics[model],
                            name: model
                        })
                    }
                }
                return series;

            },
            loadData: function () { // 获取数据库中模型训练结果
                const path = 'model/metrics?mode=' + this.featureSelected;
                if (this.chartSelected && this.featureSelected) {
                    //数据加载中
                    let DrawChart = this.$echarts.init(document.getElementById('Graph'));
                    DrawChart.showLoading();

                    //传给后端特征，获取不同模型性能
                    let _t = this;
                    this.axios.get(path).then(function (response) {
                        // console.log(response.data.code);
                        if (response.data.code === 2) {
                            _t.$message.error('Request failed!');
                        } else if (response.data.code === 1) {
                            _t.$message.error('Empty data!');
                        } else if (response.data.code === 0) {
                            _t.metrics = response.data.data;
                            for (let model in _t.metrics) {
                                _t.legend.push(model);
                            }
                            //根据用户选择的图表类型进行画图
                            _t.draw(DrawChart);
                        }
                    })
                } else {
                    this.$message.error('Please choose the features!');
                }
            },
        }
    }
</script>

<style scoped>
  .title {
    color: #ff9f43;
    font-family: bungee, sans-serif;
    font-weight: 800;
    font-size: xx-large;
    margin-bottom: 45px;
  }

  #Graph {
    width: 1000px;
    height: 400px;
    margin: auto;
    margin-top: 30px;
  }
</style>
