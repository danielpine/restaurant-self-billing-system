<template>
  <div class="index-container">
    <a-card style="width: 800px; margin: 0 auto;">
      <div style="background: #1890ff;">
        <a-row>
          <a-col :span="6">
            <h3 style="color: white;">
              <vab-icon :icon="'money-cny-box-line'"></vab-icon>
              充值中心
            </h3>
          </a-col>
        </a-row>
        <a-row style="width: 100%; color: white; font-size: 8px;">
          1.本次充值后余额永久有效。
        </a-row>
        <a-row style="width: 100%; color: white; font-size: 8px;">
          2.本次充值后立即到账，不支持退费服务。
        </a-row>
      </div>
      <a-card style="width: 100%; margin: 0 auto;">
        <a-row style="background: lightblue; line-height: 60px;">
          <a-col :span="8" style="padding-left: 10px;">
            <vab-icon :icon="'user-line'"></vab-icon>
            充值账号 :
            <span style="color: blue;">{{ username }}</span>
          </a-col>
          <a-col
            :span="8"
            :offset="8"
            style="text-align: right; padding-right: 10px;"
          >
            <vab-icon :icon="'money-cny-circle-line'"></vab-icon>
            当前余额： 1000
          </a-col>
        </a-row>
        <br />
        <br />
        <a-row class="charge">
          <a-col :span="4" style="padding-left: 10px;">
            <vab-icon :icon="'projector-line'"></vab-icon>
            充值项目：
          </a-col>
          <a-col :span="20">
            <a-radio-group :value="amount" size="large" @change="onChange">
              <a-radio-button :value="1500">
                <div>
                  充1000元
                </div>
                <div style="font-size: 16px; color: orange;">
                  赠送500元
                </div>
              </a-radio-button>
              <a-radio-button :value="1100">
                <div>
                  充800元
                </div>
                <div style="font-size: 16px; color: orange;">
                  赠送300元
                </div>
              </a-radio-button>
              <a-radio-button :value="800">
                <div>
                  充600元
                </div>
                <div style="font-size: 16px; color: orange;">
                  赠送200元
                </div>
              </a-radio-button>
              <a-radio-button :value="600">
                <div>
                  充500元
                </div>
                <div style="font-size: 16px; color: orange;">
                  赠送100元
                </div>
              </a-radio-button>
              <a-radio-button :value="350">
                <div>
                  充300元
                </div>
                <div style="font-size: 16px; color: orange;">
                  赠送50元
                </div>
              </a-radio-button>
              <a-radio-button :value="220">
                <div>
                  充200元
                </div>
                <div style="font-size: 16px; color: orange;">
                  赠送20元
                </div>
              </a-radio-button>
            </a-radio-group>
          </a-col>
        </a-row>
        <br />
        <a-row class="charge">
          <a-col :span="4" style="padding-left: 10px;">
            <vab-icon :icon="'money-cny-circle-line'"></vab-icon>
            支付金额：
          </a-col>
          <a-col :span="6" style="padding-left: 10px;">
            <span style="font-size: 30px; color: blue;">{{ pay }}</span>
            元
          </a-col>
        </a-row>
        <br />
        <a-row class="pay">
          <a-col :span="4" style="padding-left: 10px;">
            <vab-icon :icon="'bank-card-line'"></vab-icon>
            支付方式：
          </a-col>
          <a-col :span="20">
            <div>
              <a-radio-group default-value="a" size="large">
                <a-radio-button value="a">
                  <vab-icon :icon="'alipay-line'"></vab-icon>
                  支付宝
                </a-radio-button>
                <a-radio-button value="b">
                  <vab-icon :icon="'wechat-pay-line'"></vab-icon>
                  微信支付
                </a-radio-button>
              </a-radio-group>
            </div>
          </a-col>
        </a-row>
        <br />
        <br />
        <a-row>
          <a-button type="primary" style="margin: 0 auto;">
            立即充值
          </a-button>
        </a-row>
        <br />
        <br />
      </a-card>
    </a-card>
  </div>
</template>

<script>
  import VabIcon from '@/layout/vab-icon'
  import { useStore } from 'vuex'
  import { computed } from 'vue'
  export default {
    name: 'Index',
    components: { VabIcon },
    setup() {
      const store = useStore()
      return {
        username: computed(() => store.getters['user/username']),
      }
    },
    data() {
      return {
        charges: {
          1500: {
            act: 1500,
            gift: 500,
            pay: 1000,
          },
          1100: {
            act: 1100,
            gift: 300,
            pay: 800,
          },
          800: {
            act: 800,
            gift: 200,
            pay: 600,
          },
          600: {
            act: 600,
            gift: 100,
            pay: 500,
          },
          350: {
            act: 350,
            gift: 50,
            pay: 300,
          },
          220: {
            act: 220,
            gift: 20,
            pay: 200,
          },
        },
        amount: 1500,
        pay: 1000,
      }
    },
    methods: {
      onChange: function (e) {
        this.amount = e.target.value
        this.pay = this.charges[this.amount].pay
      },
    },
  }
</script>
<style lang="less">
  .charge .ant-radio-group-large .ant-radio-button-wrapper {
    height: 53px;
    width: 155px;
    margin: 10px;
    font-size: 18px;
    line-height: 25px;
    text-align: center;
    color: #000;
  }
  .pay .ant-radio-group-large .ant-radio-button-wrapper {
    width: 110px;
    height: 33px;
    line-height: 33px;
    font-size: 13px;
    margin: 10px;
    text-align: center;
    color: #000;
  }
  .ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled) {
    background: url('~@/assets/charge_checked.jpg') no-repeat;
    background-size: 100% 100%;
  }
  .ant-btn {
    width: 200px;
    height: 45px;
    border-radius: 99px;
  }
</style>
