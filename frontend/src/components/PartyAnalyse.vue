<template>
  <div id="party-analyse">
    <el-container>
        <main-header></main-header>
      <el-main>
        <el-row type="flex" justify="center">
          <h1>{{pname}}</h1>
        </el-row>
        <el-row>
          <el-col :span="6">
            <div class="yearSelected1">
              <el-select v-model="yearSelected1" placeholder="选择起始年份">
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
            <div class="yearSelected2">
              <el-select v-model="yearSelected2" placeholder="选择结束年份">
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
            <el-select class="graph-select" v-model="graphSelected" placeholder="选择图表类型">
              <el-option
                v-for="item in graphs"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>
          <el-col>
            <el-button @click="loadData" round class="button">画图</el-button>
          </el-col>
        </el-row>
        <div id="Graph"></div>
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
    name: 'PartyAnalyse',
    components: {
      'main-header': MainHeader
    },
    data() {
      return {
        yearSelected1: '',
        yearSelected2: '',
        graphSelected: '',
        graphs: [
          {label: '堆叠面积图', value: '1'},
          {label: '堆叠折线图', value: '2'},
          {label: '柱状图', value: '3'},
          {label: '极坐标堆叠柱状图', value: '4'},
        ],
        years: [
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
        pname: '',
        yearList: [],
        True: [],
        MostlyTrue: [],
        HalfTrue: [],
        MostlyFalse: [],
        False: []
      }
    },
    mounted() {
      // this.drawPic();
    },
    //获取/partyChoice传来的参数并存到pname里
    created() {
      let self = this;
      self.getParams()
    },
    watch: {
      '$route': 'getParams'
    },
    methods: {
      getParams() {
        this.pname = this.$route.query.pname;
        // console.log(this.pname);
      },
      draw: function (DrawChart) {
        // console.log(a);
        if (this.graphSelected == 1) {
          DrawChart.clear();
          var series = [];
          for (var i = 0; i < this.yearList.length; i++) {
            series.push({
              name: this.yearList[i],
              type: 'line',
              stack: '总量',
              areaStyle: {},
              data: [this.True[i], this.MostlyTrue[i], this.HalfTrue[i], this.MostlyFalse[i], this.False[i]]
            })
          }
          var option = {
            color: ['#60acfc', '#39B3EA', '#32d3eb', '#41CEC7', '#5bc49f', '#D4EC58', '#feb64d', '#FA816D', '#ff7c7c', '#D660A8', '#9287e7', '#668ED7'],
            title: {
              text: ''
            },
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
              data: this.yearList
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
                data: ['True', 'Mostly True', 'Half Ture', 'Mostly False', 'False']
              }
            ],
            yAxis: [
              {
                type: 'value'
              }
            ],
            series: series
          };
          DrawChart.hideLoading();
          DrawChart.setOption(option);
        } else if (this.graphSelected == 2) {
          DrawChart.clear();
          var series = [];
          for (var i = 0; i < this.yearList.length; i++) {
            series.push({
              name: this.yearList[i],
              type: 'line',
              stack: '总量',
              data: [this.True[i], this.MostlyTrue[i], this.HalfTrue[i], this.MostlyFalse[i], this.False[i]]
            })
          }
          var option = {
            color: ['#60acfc', '#39B3EA', '#32d3eb', '#41CEC7', '#5bc49f', '#D4EC58', '#feb64d', '#FA816D', '#ff7c7c', '#D660A8', '#9287e7', '#668ED7'],

            title: {
              text: ''
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: this.yearList
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            toolbox: {
              feature: {
                saveAsImage: {}
              }
            },
            xAxis: {
              type: 'category',
              boundaryGap: false,
              data: ['True', 'Mostly True', 'Half True', 'Mostly False', 'False']
            },
            yAxis: {
              type: 'value'
            },
            series: series
          }
          DrawChart.hideLoading();
          DrawChart.setOption(option);
        } else if (this.graphSelected == 3) {
          DrawChart.clear();
          var option = {
            // color: ['#1e3799', '#4a69bd', '#6a89cc', '#fa983a', '#eb2f06'],
            color: ['#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c'],
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'shadow'
              }
            },
            legend: {
              data: ['True', 'Mostly True', 'Half True', 'Mostly False', 'False']
            },
            toolbox: {
              show: true,
              orient: 'vertical',
              left: 'right',
              top: 'center',
              feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar', 'stack']},
                restore: {show: true},
                saveAsImage: {show: true}
              }
            },
            calculable: true,
            xAxis: [
              {
                type: 'category',
                axisTick: {show: false},
                data: this.yearList
              }
            ],
            yAxis: [
              {
                type: 'value'
              }
            ],
            series: [
              {
                name: 'True',
                type: 'bar',
                barGap: 0,
                data: this.True
              },
              {
                name: 'Mostly True',
                type: 'bar',
                data: this.MostlyTrue
              },
              {
                name: 'Half True',
                type: 'bar',
                data: this.HalfTrue
              },
              {
                name: 'Mostly False',
                type: 'bar',
                data: this.MostlyFalse
              },
              {
                name: 'False',
                type: 'bar',
                data: this.False
              }
            ]
          };
          DrawChart.hideLoading();
          DrawChart.setOption(option);
        } else if (this.graphSelected == 4) {
          DrawChart.clear();
          var option = {
            color: ['#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c'],
            angleAxis: {},
            radiusAxis: {
              type: 'category',
              data: this.yearList,
              z: 10
            },
            polar: {},
            toolbox: {
              show: true,
              orient: 'vertical',
              left: 'right',
              top: 'center',
              feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
              }
            },
            series: [{
              type: 'bar',
              data: this.True,
              coordinateSystem: 'polar',
              name: 'True',
              stack: 'a'
            }, {
              type: 'bar',
              data: this.MostlyTrue,
              coordinateSystem: 'polar',
              name: 'Mostly True',
              stack: 'a'
            }, {
              type: 'bar',
              data: this.HalfTrue,
              coordinateSystem: 'polar',
              name: 'Half True',
              stack: 'a'
            }, {
              type: 'bar',
              data: this.MostlyFalse,
              coordinateSystem: 'polar',
              name: 'Mostly False',
              stack: 'a'
            }, {
              type: 'bar',
              data: this.False,
              coordinateSystem: 'polar',
              name: 'False',
              stack: 'a'
            },],
            legend: {
              show: true,
              data: ['True', 'Mostly True', 'Half Ture', 'Mostly False', 'False']
            }
          }
          DrawChart.hideLoading();
          DrawChart.setOption(option);
        }
      },
      loadData: function () {
        var year1 = this.yearSelected1;
        var year2 = this.yearSelected2;
        //清空
        this.yearList = [];
        var year = this.yearList;
        // console.log(year1,year2)
        if (year1 <= year2) {
          do {
            this.yearList.push(year1);
            // console.log(yearList);
            year1 = year1 + 1;
          } while (year1 <= year2);
          // console.log(yearList)
          const path = 'ch/party?party=' + this.pname + '&year1=' + this.yearSelected1 + '&year2=' + this.yearSelected2;
          // const path = 'ch/year?year=2017'
          var _t = this;
          _t.True = [];
          _t.MostlyTrue = [];
          _t.HalfTrue = [];
          _t.MostlyFalse = [];
          _t.False = [];

          var DrawChart = this.$echarts.init(document.getElementById('Graph'));
          DrawChart.showLoading();
          this.axios.get(path).then(function (response) {
            if (response.data.code === 2) {
              _t.$message.error('Request failed!');
            } else if (response.data.code === 1) {
              _t.$message.error('Empty data!');
            } else if (response.data.code === 0) {
              let d = response.data.data;
              console.log(d);
              console.log(year);
              _t.True = d.map((x, index) => x[year[index]]['TrueCounts']);
              _t.MostlyTrue = d.map((x, index) => x[year[index]]['mostlyTrueCounts']);
              _t.HalfTrue = d.map((x, index) => x[year[index]]['halfTrueCounts']);
              _t.MostlyFalse = d.map((x, index) => x[year[index]]['mostlyFalseCounts']);
              _t.False = d.map((x, index) => x[year[index]]['FalseCounts']);

              //根据用户选择的图表类型进行画图
              _t.draw(DrawChart);
            }
          })
        }
        // 输入错误
        else {
          this.$message.error('Please enter again!');
        }
      }
    }
  }
</script>
<style scoped>
  #graph-select {
    width: auto;
  }

  #Graph {
    width: 1000px;
    height: 400px;
    margin: auto;
    margin-top: 50px;
  }

  .el-col {
    width: 210px;
  }

  .el-row {
    padding-top: 20px;
    padding-left: 290px;
    padding-right: 250px;
  }
</style>
