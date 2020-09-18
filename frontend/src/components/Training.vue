<template>
  <div id="model-comparison">
    <el-container>
      <main-header></main-header>
      <el-main>
        <el-row type="flex" justify="center">
          <h1 class="title">重新训练模型</h1>
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
            <span>模型选择</span>
            <el-select v-model="modelSelected" placeholder="请选择一个模型">
              <el-option
                v-for="sm in supportedModels"
                :key="sm"
                :label="sm"
                :value="sm">
              </el-option>
            </el-select>
            <span>测试集占比</span>
            <el-select v-model="testSize" placeholder="请选择测试集占比">
              <el-option
                v-for="ts in testSizeRange"
                :key="ts"
                :label="ts"
                :value="ts">
              </el-option>
            </el-select>
          </el-form>
        </el-row>
        <el-row justify="center" type="flex" style="margin-top: 10px">
          <el-col :span="5">
            <el-input v-model="email" placeholder="填写邮箱，训练结果将以邮件形式告知您">
            </el-input>
          </el-col>

        </el-row>
        <el-row justify="center" type="flex" style="margin-top: 10px">
          <el-button type="warning" @click="open">训练模型</el-button>

        </el-row>
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
                modelSelected: "",
                testSize: 0.3,
                testSizeRange: [0.1, 0.2, 0.3, 0.4, 0.5],
                supportedModels: [],
                metrics: {},
                legend: [],
                email: [],
            }
        },
        mounted() {
            this.getSupportedModel();
        },
        methods: {
            getSupportedModel: function () {
                let _t = this;
                this.axios.get("model/supportedModel").then(function (resp) {
                    if (resp.data.code === 2) {
                        _t.$message("Request failed, plz check the param");
                        return;
                    }
                    _t.supportedModels = resp.data.data;
                })
            },
            train: function () { // 用最新的数据重新训练模型
                const path = 'model/train?model_name=' + this.modelSelected +
                    "&mode=" + this.featureSelected + "&test_size=" + this.testSize
                    + "&email=" + this.email;
                let _t = this;
                this.axios.get(path).then(function (response) {
                    if (response.data.code === 3) {
                        _t.$message.error("Insufficient permissions.")
                    }
                    if (response.data.code === 2) {
                        _t.$message.error('Request failed!');
                    } else if (response.data.code === 0) {
                        if (response.data.data.status === "success") {
                            _t.$message({
                                message: 'Model training Task has submitted successfully. Plz Check you email to get training results.',
                                type: 'success'
                            });
                        } else {
                            _t.$message.error('Model training failed!');
                        }
                    }
                })
            },
            open: function () {
                if (this.featureSelected.length === 0 || this.modelSelected.length === 0) {
                    this.$message({
                        message: "plz check the param",
                        type: "error"
                    });
                    return;
                }
                this.$confirm('The model would be re-trained, are you sure?', 'Warning', {
                    confirmButtonText: 'Confirm',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    this.train();
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: 'Cancelled!'
                    });
                });
            }
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
</style>
