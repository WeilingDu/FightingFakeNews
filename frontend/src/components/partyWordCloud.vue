<template>
  <div id="party-wordcloud">
    <el-container>
        <main-header></main-header>
      <el-main>
        <el-row justify="center" type="flex">
          <h1>党派 : {{pname}}</h1>
        </el-row>
        <el-row justify="center">
          <el-col :span="5" :offset="8">
              <el-select v-model="yearSelected" placeholder="请选择一个年份">
                    <el-option
                      v-for="item in years"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
              </el-select>
          </el-col>
          <el-button @click="drawCloud" round type="primary">画图</el-button>

        </el-row>
        <div id="WordCloud" style="width: 1200px;height: 600px;margin-top: 30px;margin-left: auto;margin-right:auto"></div>
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
  name: 'partyWordCloud',
  components:{
    'main-header':MainHeader
  },
  data () {
    return {
      yearSelected:'',
      pname:'',
      serverResponse:'',
      years:[
        {value:0,label:'全部'},
        {value:2009,label:2009},
        {value:2010,label:2010},
        {value:2011,label:2011},
        {value:2012,label:2012},
        {value:2013,label:2013},
        {value:2014,label:2014},
        {value:2015,label:2015},
        {value:2016,label:2016},
        {value:2017,label:2017},
        {value:2018,label:2018},
        {value:2019,label:2019},
      ],
    }
  },
  mounted(){
  },
  //获取/choiceCloudp传来的参数并存到sname里
  created () {
    let self = this
    self.getParams()
    },
  watch: {
  '$route': 'getParams'
  },
  methods:{
    getParams () {
    this.pname = this.$route.query.pname;
    // console.log(this.pname);
    },
    drawCloud:function(){
      var wordCloud = this.$echarts.init(document.getElementById('WordCloud'))
      // 先清空图例
      wordCloud.setOption({}, true)
      var that = this;
      const path = 'wordcnt/party?party=' + this.pname + '&year=' + this.yearSelected;
      // const path = 'wordcnt/speaker?sname=' + this.sname + '&year=' + this.yearSelected;
      // const path = 'wordcnt/speaker?sname=Donald Trump&year=2015';
      //const path = 'wordcnt/speaker?sname=Donald Trump';
      this.axios.get(path).then(function(response){
        // console.log(response);
        if(response.data.code == 2){
          that.$message.error('Request failed!');
        }
        else if (response.data.code == 1) {
          that.$message({
          message: 'Empty data!',
          center: true
          })
        }
        else if (response.data.code == 0) {
          var d = response.data.data;
          var option = {
            title: {
                text: "WordCloud by Party"
            },
            tooltip: {},
            series: [{
                type: 'wordCloud',
                // gridSize: 20,
                gridSize: 20,
                // sizeRange: [12, 50],
                sizeRange: [25, 75],
                rotationRange: [0, 0],
                shape: 'circle',
                textStyle: {
                    normal: {
                        color: function() {
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
                        // shadowColor: '#333'
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

#WordCloud{
  width: 100%;
  height: 800px;
}

</style>
