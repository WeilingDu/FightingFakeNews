<template>
  <div id="main-page" style="overflow : hidden">
    <main-header></main-header>
    <div>
      <div style="text-align: center;">
        <h1 style="color: #ff9f43; font-family: bungee, sans-serif; font-weight: 800; font-size: xx-large">Fake News
          Visualization</h1>
      </div>
    </div>
    <div
      id="Picture"
      style="width: 800px;height: 400px;margin-top: 30px;margin-left: auto;margin-right:auto"
    >
    </div>
  </div>
</template>
<style>
  body {
    margin: 0 0 0 0;
  }
</style>
<script>
    import MainHeader from './MainHeader'
    import echarts from 'echarts/lib/echarts'

    export default {
        name: 'MainPage',
        components: {
            'main-header': MainHeader
        },
        data() {
            return {
                // year1:2009,
                // year2:2019,
                yearList: [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
                dataCounts: []
            }
        },
        mounted() {
            this.DrawPic();
        },
        methods: {
            DrawPic: function () {
                var DrawChart = this.$echarts.init(document.getElementById('Picture'));
                var myData = ['True', 'Mostly True  ', 'Half True  ', 'Mostly False  ', 'False', 'On Fire  '];
                var _t = this;
                const path = 'ch/year?year1=2009&year2=2019';
                this.axios.get(path).then(function (response) {
                    if (response.data.code == 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code == 1) {
                        _t.$message.error('Empty data!');
                    } else if (response.data.code == 0) {
                        // console.log(response.data.data);
                        var year = _t.yearList;
                        for (var x in response.data.data) {
                            var d = [];
                            d.push(response.data.data[x][year[x]]['TrueCounts']);
                            d.push(response.data.data[x][year[x]]['mostlyTrueCounts']);
                            d.push(response.data.data[x][year[x]]['halfTrueCounts']);
                            d.push(response.data.data[x][year[x]]['mostlyFalseCounts']);
                            d.push(response.data.data[x][year[x]]['FalseCounts']);
                            d.push(response.data.data[x][year[x]]['onFireCounts']);
                            // console.log(d);
                            _t.dataCounts.push(d);
                        }
                        // console.log(_t.dataCounts[0]);
                        // console.log(_t.dataCounts[0][0]);
                        var timeLineData = _t.yearList;
                        var data = [];
                        for (var k in _t.dataCounts) {
                            var c = [];
                            c.push(_t.dataCounts[k][0])
                            c.push(_t.dataCounts[k][1])
                            c.push(_t.dataCounts[k][2])
                            c.push(_t.dataCounts[k][3])
                            c.push(_t.dataCounts[k][4])
                            c.push(_t.dataCounts[k][5])
                            data.push(c);
                        }
                        var FinalData = {
                            2009: data[0],
                            2010: data[1],
                            2011: data[2],
                            2012: data[3],
                            2013: data[4],
                            2014: data[5],
                            2015: data[6],
                            2016: data[7],
                            2017: data[8],
                            2018: data[9],
                            2019: data[10],
                        }
                        // console.log(data);
                        var option = {
                            baseOption: {
                                backgroundColor: '#fff',
                                timeline: {
                                    show: true,
                                    axisType: 'category',
                                    tooltip: {
                                        show: true,
                                        formatter: function (params) {
                                            console.log(params);
                                            return params.name;
                                        }
                                    },
                                    autoPlay: true,
                                    currentIndex: 6,
                                    playInterval: 1000,
                                    label: {
                                        normal: {
                                            show: true,
                                            interval: 'auto',
                                            formatter: '{value}',
                                        },
                                    },
                                    data: [],
                                },
                                title: {
                                    textStyle: {
                                        // color: '#000',
                                        color: '#57606f',
                                        fontFamily: 'pt-sans-caption, sans-serif',
                                        fontSize: 16,
                                    },
                                    subtext: '',
                                },
                                tooltip: {
                                    show: true,
                                    trigger: 'axis',
                                    formatter: '{b}<br/>{a}: {c}',
                                    axisPointer: {
                                        type: 'shadow',
                                    }
                                },

                                toolbox: {
                                    right: 20,
                                    feature: {
                                        saveAsImage: {},
                                        restore: {},
                                        dataView: {},
                                        dataZoom: {},
                                        magicType: {
                                            type: ['line', 'bar']
                                        },
                                        // brush: {},
                                    }
                                },

                                grid: [{
                                    show: false,
                                    left: '20%',
                                    top: 80,
                                    bottom: 60,
                                    width: '0%',
                                }, {
                                    show: false,
                                    left: '25%',
                                    top: 60,
                                    bottom: 60,
                                    containLabel: true,
                                    width: '46%',
                                },],

                                xAxis: [{
                                    show: false,
                                }, {
                                    gridIndex: 1,
                                    type: 'value',
                                    axisLine: {
                                        show: false,
                                    },
                                    axisTick: {
                                        show: false,
                                    },
                                    position: 'top',
                                    axisLabel: {
                                        show: true,
                                        textStyle: {
                                            // color: '#000',
                                            color: '#57606f',
                                            fontFamily: 'pt-sans-caption, sans-serif',
                                            fontSize: 12,
                                        },
                                    },
                                    splitLine: {
                                        show: true,
                                        lineStyle: {
                                            color: '#b2bec3',
                                            width: 1,
                                            type: 'solid',
                                        },
                                    },
                                },],
                                yAxis: [{
                                    type: 'category',
                                    inverse: true,
                                    position: 'left',
                                    axisLine: {
                                        show: false
                                    },
                                    axisTick: {
                                        show: false
                                    },
                                    axisLabel: {
                                        show: true,
                                        textStyle: {
                                            // color: '#000',
                                            color: '#57606f',
                                            fontFamily: 'pt-sans-caption, sans-serif',
                                            fontSize: 16,
                                        },

                                    },
                                    data: myData.map(function (value) {
                                        return {
                                            value: value,
                                            textStyle: {
                                                align: 'center',
                                            }
                                        }
                                    }),
                                }, {
                                    gridIndex: 1,
                                    type: 'category',
                                    inverse: true,
                                    position: 'left',
                                    axisLine: {
                                        show: false
                                    },
                                    axisTick: {
                                        show: false
                                    },
                                    axisLabel: {
                                        show: false,
                                        textStyle: {
                                            color: '#9D9EA0',
                                            fontSize: 12,
                                        },

                                    },
                                    data: myData,
                                },],
                                series: [],

                            },
                            options: [],
                        }
                        for (var i = 0; i < timeLineData.length; i++) {
                            option.baseOption.timeline.data.push(timeLineData[i]);
                            option.options.push({
                                title: {
                                    text: timeLineData[i] + ' True or False Statistics',
                                },
                                series: [
                                    {
                                        name: 'Counts',
                                        type: 'bar',
                                        barWidth: 25,
                                        xAxisIndex: 1,
                                        yAxisIndex: 1,
                                        label: {
                                            normal: {
                                                show: false,
                                            },
                                            emphasis: {
                                                show: true,
                                                // position: 'left',
                                                position: 'right',
                                                // offset: [0, 0],
                                                offset: [50, 0],
                                                textStyle: {
                                                    // color: '#000',
                                                    color: '#57606f',
                                                    fontFamily: 'pt-sans-caption, sans-serif',
                                                    fontSize: 14,
                                                },
                                            },
                                        },
                                        itemStyle: {
                                            normal: {
                                                color: new echarts.graphic.LinearGradient(
                                                    0, 0, 0, 1,
                                                    [
                                                        {offset: 0, color: '#83bff6'},
                                                        {offset: 0.5, color: '#188df0'},
                                                        {offset: 1, color: '#188df0'}
                                                    ]
                                                ),
                                            },
                                            emphasis: {
                                                color: new echarts.graphic.LinearGradient(
                                                    0, 0, 0, 1,
                                                    [
                                                        {offset: 0, color: '#2378f7'},
                                                        {offset: 0.7, color: '#2378f7'},
                                                        {offset: 1, color: '#83bff6'}
                                                    ]
                                                ),
                                            },
                                        },
                                        data: FinalData[timeLineData[i]],
                                    }
                                ]
                            });
                        }
                        DrawChart.setOption(option);
                    }
                })
            }
        }
    }
</script>
