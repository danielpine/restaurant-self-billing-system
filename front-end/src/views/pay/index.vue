<template>
  <div class="example">
    <a-drawer
      title="Pay"
      placement="right"
      :width="520"
      :closable="false"
      :visible="modalVisible"
      :get-container="false"
      @close="onModalClose"
      class="settings"
      v-if="currOrder && currOrder.sum"
    >
      <a-card
        style="width: 100%; height: 70%; text-align: center"
        :tab-list="tabListNoTitle"
        :active-tab-key="noTitleKey"
        @tabChange="(key) => onTabChange(key, 'noTitleKey')"
      >
        <a-row>
          <div style="width: 250px; margin: 0 auto">
            <a-row v-for="(v, i) in currOrder.items" :key="i">
              <a-col :span="12" style="text-align: left">
                <span>{{ v.type }}</span>
              </a-col>
              <a-col :span="6"></a-col>
              <a-col :span="6" style="text-align: right">
                <span>{{ v.unit + 'x' + v.count }}</span>
              </a-col>
            </a-row>
            <a-divider dashed></a-divider>
            <a-row>
              <a-col :span="12" style="text-align: left">应付：</a-col>
              <a-col :span="6"></a-col>
              <a-col :span="6" style="text-align: right">
                {{ '¥' + currOrder.sum }}
              </a-col>
            </a-row>
            <a-row>
              <a-col :span="12" style="text-align: left">折扣：</a-col>
              <a-col :span="6"></a-col>
              <a-col :span="6" style="text-align: right">
                <span v-if="role == 'visitor' || discount <= 5">无</span>
                <span
                  v-if="role != 'visitor' && discount > 5 && discount <= 10"
                >
                  9.5折
                </span>
                <span v-if="role != 'visitor' && discount > 10">9折</span>
              </a-col>
            </a-row>
            <a-row>
              <a-col :span="12" style="text-align: left">优惠：</a-col>
              <a-col :span="6"></a-col>
              <a-col :span="6" style="text-align: right">
                {{ '¥' + (currOrder.sum - currOrder.pay) }}
              </a-col>
            </a-row>
            <a-row>
              <a-col :span="12" style="text-align: left">实付：</a-col>
              <a-col :span="6"></a-col>
              <a-col :span="6" style="text-align: right">
                {{ '¥' + currOrder.pay }}
              </a-col>
            </a-row>
          </div>
          <a-divider></a-divider>
        </a-row>
        <div
          v-if="noTitleKey === '余额支付' && role == 'member'"
          style="margin: 0 auto"
        >
          <div style="width: 250px; margin: 0 auto">
            <a-row class="charge">
              <a-col :span="12" style="text-align: left">
                <vab-icon :icon="'money-cny-circle-line'"></vab-icon>
                当前余额：
              </a-col>
              <a-col :span="12" style="text-align: right">
                <span style="font-size: 30px; color: #1890ff">
                  {{ balance }}
                </span>
                元
              </a-col>
            </a-row>
          </div>
          <div style="width: 250px; margin: 0 auto">
            <a-row class="charge" v-if="balance >= currOrder.sum">
              <a-col :span="12" style="text-align: left">
                <vab-icon :icon="'money-cny-circle-line'"></vab-icon>
                本次扣款：
              </a-col>
              <a-col :span="12" style="text-align: right">
                <span style="font-size: 30px; color: #1890ff">
                  {{ currOrder.pay }}
                </span>
                元
              </a-col>
            </a-row>
            <a-row v-else style="color: orange">
              <vab-icon :icon="'alert-line'"></vab-icon>
              &nbsp;余额不足请充值或扫描付款！
            </a-row>
          </div>
          <br />
        </div>
        <div
          v-else-if="noTitleKey === '余额支付' && role == 'visitor'"
          style="margin: 0 auto"
        >
          <div style="width: 250px; margin: 0 auto">
            <a-row style="color: orange">
              <vab-icon :icon="'alert-line'"></vab-icon>
              &nbsp;游客请用扫码支付，或加入会员！
            </a-row>
          </div>
          <br />
        </div>
        <div v-else-if="noTitleKey === '扫码支付'" style="margin: 0 auto">
          <div>
            <qrcode-vue :value="qrCodeUrl" :size="250" level="H" />
          </div>
          <div>
            <p>支付宝或微信扫一扫支付</p>
            <a-button style="margin: 0 auto" type="primary" @click="pay('qr')">
              <vab-icon :icon="'check-fill'"></vab-icon>
              模拟扫码
            </a-button>
          </div>
        </div>
        <a-row v-if="noTitleKey === '余额支付'">
          <a-button
            style="margin: 0 auto"
            type="primary"
            :disabled="balance < currOrder.sum"
            @click="pay('balance')"
          >
            <vab-icon :icon="'check-fill'"></vab-icon>
            立即支付
          </a-button>
        </a-row>
      </a-card>
    </a-drawer>
    <a-drawer
      title="Settings"
      placement="right"
      :width="520"
      :closable="false"
      :visible="visible"
      :get-container="false"
      @close="onClose"
      class="settings"
    >
      <a-row>
        <a-col :span="4">Threshold1</a-col>
        <a-col :span="20">
          <a-slider
            :default-value="config.threshold1"
            @change="threshold1Change"
          />
        </a-col>
      </a-row>
      <a-row>
        <a-col :span="4">Threshold2</a-col>
        <a-col :span="20">
          <a-slider
            :default-value="config.threshold2"
            @change="threshold2Change"
          />
        </a-col>
      </a-row>
      <a-row>
        <a-col :span="4">FrontScale</a-col>
        <a-col :span="20">
          <a-slider
            :default-value="config.frontScale"
            @change="frontScaleChange"
          />
        </a-col>
      </a-row>
      <a-row>
        <a-col :span="4">BackScale</a-col>
        <a-col :span="20">
          <a-slider
            :default-value="config.backScale"
            @change="backScaleChange"
          />
        </a-col>
      </a-row>
      <a-row>
        <a-col :span="4">AreaRange</a-col>
        <a-col :span="20">
          <a-slider
            range
            :default-value="[config.minArea, config.maxArea]"
            :min="0"
            :max="100000"
            @change="areaChange"
          />
        </a-col>
      </a-row>
      <a-row style="margin-top: 10px">
        <a-col :span="5">KernelSize</a-col>
        <a-col :span="19">
          <a-input-number
            :default-value="config.kernelSize"
            :min="1"
            :max="1000"
            @change="kernelSizeChange"
          />
        </a-col>
      </a-row>
      <a-row style="margin-top: 10px">
        <a-col :span="5">GaussianSize</a-col>
        <a-col :span="19">
          <a-input-number
            :default-value="config.gaussianSize"
            :min="1"
            :max="1000"
            :step="2"
            @change="gaussianSizeChange"
          />
        </a-col>
      </a-row>
      <a-row style="margin-top: 10px">
        <a-col :span="5">DetectCount</a-col>
        <a-col :span="19">
          <a-input-number
            :default-value="config.detectCount"
            :min="3"
            :max="20"
            @change="detectCountChange"
          />
        </a-col>
      </a-row>
      <pre> {{ JSON.stringify(config, null, 4) }} </pre>
    </a-drawer>
    <a-spin
      class="content"
      :spinning="!imgShow"
      size="small"
      tip="拼命加载中..."
    />
    <a-row type="flex" v-show="imgShow || step == 1">
      <a-col flex="600px">
        <div>
          <img
            v-show="imgShow"
            :src="imgSrc"
            :width="width"
            :height="height"
            id="photo"
            @load="onload"
          />
          <video
            v-show="!imgShow"
            id="video"
            class="src-video"
            :width="width"
            :height="height"
            autoplay="autoplay"
          ></video>
        </div>
      </a-col>
      <a-col flex="auto" style="text-align: center">
        <a-button
          type="dashed"
          shape="circle"
          class="fix-top-right"
          @click="showDrawer"
        >
          <vab-icon :icon="'bug-line'"></vab-icon>
        </a-button>
        <a-card
          title="合并订单"
          :headStyle="{ background: 'aliceblue' }"
          :bordered="true"
          style="width: 450px; margin-left: 50px; background: white"
          :style="{ height: height + 'px' }"
        >
          <div :style="{ height: height - 150 + 'px' }" class="parent">
            <span v-if="step == 1" class="child">
              <a-alert message="请放入菜品..." banner />
            </span>
            <span v-if="step == 4" class="child">
              <a-alert message="请移走餐盘..." banner />
            </span>
            <span v-if="step == 2" class="child">
              <a-spin :spinning="step == 2" size="large" tip="正在识别..." />
            </span>
            <div v-if="step == 3" class="dotted">
              <a-divider dashed style="height: 3px"></a-divider>
              <div class="vertical" style="width: 250px; margin: 0 auto">
                <a-row v-for="(v, i) in currOrder.items" :key="i">
                  <a-col :span="12" style="text-align: left">
                    <h3>{{ v.type }}</h3>
                  </a-col>
                  <a-col :span="1"></a-col>
                  <a-col :span="5" style="text-align: left">
                    <h3>{{ v.unit }}</h3>
                  </a-col>
                  <a-col :span="6" style="text-align: left">
                    <h3>{{ 'x' + v.count }}</h3>
                  </a-col>
                </a-row>
                <a-divider dashed></a-divider>
                <a-row>
                  <a-col :span="12" style="text-align: left">
                    <h3>合计:</h3>
                  </a-col>
                  <a-col :span="1"></a-col>
                  <a-col :span="5" style="text-align: left">
                    <h3>{{ '¥' + currOrder.sum }}</h3>
                  </a-col>
                  <a-col :span="6" style="text-align: left">
                    <h3>{{ currOrder.volume + '(份)' }}</h3>
                  </a-col>
                </a-row>
              </div>
            </div>
            <div v-if="step == 3" class="dotted-bottom"></div>
          </div>
          <a-row type="flex" v-if="step == 3">
            <a-col flex="auto" style="text-align: center">
              <a-button type="primary" @click="reDetect">重新识别</a-button>
            </a-col>
            <a-col flex="auto" style="text-align: center">
              <a-button type="primary" @click="payNow">现在支付</a-button>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>
    <canvas
      id="canvas"
      style="display: none"
      :width="width"
      :height="height"
    ></canvas>
  </div>
</template>

<script>
  import VabIcon from '@/layout/vab-icon'
  import QrcodeVue from 'qrcode.vue'
  import { useStore } from 'vuex'
  import { computed } from 'vue'
  import { getUserBalance, paymentRequest, getUserDiscount } from '@/api/user'
  import { getAccessToken } from '@/utils/accessToken'
  import { message } from 'ant-design-vue'

  export default {
    name: 'Index',
    components: { VabIcon, QrcodeVue },
    setup() {
      const store = useStore()
      return {
        avatar: computed(() => store.getters['user/avatar']),
        username: computed(() => store.getters['user/username']),
        role: computed(() => store.getters['acl/role'][0]),
      }
    },
    data() {
      return {
        step: 2, // 1 识别区为空等待放入 2 识别中  3 识别完成待支付 4 刚支付完，等待移走餐盘
        config: {
          threshold1: 74,
          threshold2: 74,
          minArea: 10000,
          maxArea: 50000,
          detectCount: 10,
          frontScale: 50,
          backScale: 70,
          kernelSize: 5,
          gaussianSize: 7,
        },
        tabListNoTitle: [
          {
            key: '余额支付',
            tab: '余额支付',
          },
          {
            key: '扫码支付',
            tab: '扫码支付',
          },
        ],
        noTitleKey: '余额支付',
        qrCodeUrl: '50元',
        width: '1200',
        height: '900',
        prefix: 'data:image/png;base64,',
        srcVideo: null,
        mediaStream: null,
        photo: null,
        webcamOpen: false,
        timer: null,
        imgSrc: null,
        imgShow: false,
        visible: false,
        modalVisible: false,
        justPay: false,
        fps: 200,
        currOrder: null,
        plates: [],
        accumulator: 0,
        balance: null,
        discount: null,
      }
    },
    created() {
      this.loadConfig()
    },
    mounted() {
      this.initSource()
      this.createWebSocket()
    },
    unmounted() {
      this.closeMedia()
    },
    methods: {
      payNow() {
        if (this.role == 'member') {
          this.getUserBalance()
          this.getUserDiscount()
        } else if (this.role == 'visitor') {
          this.discount = 0
          this.currOrder.discount = 1
          this.currOrder.pay = this.currOrder.sum
        }
        this.modalVisible = true
      },
      pay(mode) {
        this.paymentRequest(this.currOrder, mode)
      },
      async paymentRequest(order, mode) {
        await paymentRequest(getAccessToken(), order, mode)
        message.info('支付成功,请移走餐盘！')
        this.modalVisible = false
        this.justPay = true
        this.createTimer()
      },
      async getUserBalance() {
        let { data } = await getUserBalance(getAccessToken())
        this.balance = data
      },
      async getUserDiscount() {
        let { data } = await getUserDiscount(getAccessToken())
        this.discount = data
        if (this.discount <= 5) {
          this.currOrder['discount'] = 1
        } else if (this.discount > 5 && this.discount <= 10) {
          this.currOrder['discount'] = 0.95
        } else if (this.discount > 10) {
          this.currOrder['discount'] = 0.9
        }
        this.currOrder['pay'] = parseFloat(
          (this.currOrder.sum * this.currOrder.discount).toFixed(2)
        )
      },
      onTabChange(key, type) {
        this[type] = key
      },
      loadConfig() {
        let cache = window.localStorage.getItem('config')
        if (cache) {
          cache = JSON.parse(cache)
          for (const key in cache) {
            this.config[key] = cache[key]
          }
        }
      },
      saveConfig() {
        window.localStorage.setItem('config', JSON.stringify(this.config))
      },
      frontScaleChange(val) {
        this.config.frontScale = val
        this.saveConfig()
      },
      backScaleChange(val) {
        this.config.backScale = val
        this.saveConfig()
      },
      kernelSizeChange(val) {
        this.config.kernelSize = val
        this.saveConfig()
      },
      gaussianSizeChange(val) {
        this.config.gaussianSize = val
        this.saveConfig()
      },
      detectCountChange(val) {
        this.config.detectCount = val
        this.saveConfig()
      },
      threshold1Change(val) {
        this.config.threshold1 = val
        this.saveConfig()
      },
      threshold2Change(val) {
        this.config.threshold2 = val
        this.saveConfig()
      },
      areaChange(val) {
        this.config.minArea = val[0]
        this.config.maxArea = val[1]
        this.saveConfig()
      },
      afterVisibleChange(val) {
        console.log('visible', val)
      },
      showDrawer() {
        this.visible = true
      },
      onClose() {
        this.visible = false
      },
      onModalClose() {
        this.modalVisible = false
      },
      onload: function () {
        if (!this.imgShow) {
          let this_ = this
          setTimeout(function () {
            this_.imgShow = true
          }, 900)
        }
      },
      initSource: function () {
        this.srcVideo = document.getElementById('video')
        this.photo = document.getElementById('photo')
        let h = document.body.clientHeight
        let w = document.body.clientWidth
        this.width = w * 0.5
        this.height = h * 0.7
      },
      clearTimer: function () {
        if (this.timer) {
          clearTimeout(this.timer)
          console.log('timer 已清除')
        }
      },
      createTimer: function () {
        let this_ = this
        this.clearTimer()
        this.timer = setInterval(function () {
          if (this_.webcamOpen) {
            let canvas = document.getElementById('canvas')
            let ctx = canvas.getContext('2d')
            ctx.drawImage(this_.srcVideo, 0, 0, this_.width, this_.height)
            this_.videoImg = canvas.toDataURL(
              'image/jpeg',
              this_.config.frontScale / 100
            )
            var data = this_.videoImg.split(',')
            this_.ws.send(
              JSON.stringify({
                config: this_.config,
                image: data[1],
              })
            )
          }
        }, this_.fps)
      },
      processEvent: function (evt) {
        let this_ = this
        let data = JSON.parse(evt.data)
        if (data.plates.length == 0) {
          this.imgShow = true
          this.imgSrc = this_.videoImg
          this.step = 1
          this.plates = []
          this.accumulator = 0
          this.justPay = false
        } else {
          this.step = 2
        }

        if (this.justPay) {
          console.log('justPay')
          if (JSON.stringify(this.plates) == JSON.stringify(data.plates)) {
            this.accumulator = 0
            this.step = 4
            this.imgSrc = this_.prefix + data.image
          } else {
            this.justPay = false
            this.step = 2
            this.plates = []
          }
        }

        if (this.visible) {
          this.imgShow = true
          this.imgSrc = this_.prefix + data.image
        } else if (this.step == 2) {
          this.imgShow = true
          this.imgSrc = this_.prefix + data.image
          if (JSON.stringify(this.plates) == JSON.stringify(data.plates)) {
            this.accumulator++
            console.log(this.step, this.accumulator)
          } else {
            this.accumulator = 0
          }
          this.plates = data.plates
          if (this.accumulator > this.config.detectCount) {
            this.step = 3
            this.clearTimer()
            this.createOrder()
          }
        }
      },
      reDetect: function () {
        this.step == 2
        this.plates = []
        this.accumulator = 0
        this.createTimer()
      },
      createOrder: function () {
        let currOrder = {}
        let object = this.plates
        for (const key in object) {
          if (Object.hasOwnProperty.call(object, key)) {
            const item = object[key]
            console.log(item, currOrder[item])
            if (currOrder[item] == undefined) {
              currOrder[item] = 1
            } else {
              currOrder[item] = currOrder[item] + 1
            }
          }
        }
        let order = {
          items: [],
          sum: 0,
          volume: 0,
        }
        for (const key in currOrder) {
          console.log(key)
          const e = currOrder[key]
          order.volume = order.volume + e
          if (key == 'rect') {
            console.log('方形菜品 ¥5 x' + e)
            order.items.push({
              type: '方形菜品',
              unit: '¥5',
              count: e,
            })
            order.sum = order.sum + 5 * e
          } else if (key == 'eclipse') {
            console.log('椭圆菜品 ¥10 x' + e)
            order.items.push({
              type: '椭圆菜品',
              unit: '¥10',
              count: e,
            })
            order.sum = order.sum + 10 * e
          } else if (key == 'circle') {
            console.log('圆形菜品 ¥15 x' + e)
            order.items.push({
              type: '圆形菜品',
              unit: '¥15',
              count: e,
            })
            order.sum = order.sum + 15 * e
          }
        }
        this.currOrder = order
      },
      createWebSocket: function () {
        let this_ = this
        this.ws = new WebSocket('ws://' + location.host + '/socket')
        this.ws.onopen = function () {
          console.log('ws opened')
          this_.openMedia()
          console.log('media opened')
          this_.createTimer()
          console.log('timer created')
        }
        this.ws.onmessage = function (evt) {
          this_.processEvent(evt)
        }
        this.ws.onclose = function () {
          console.log('Closed')
        }
        this.ws.onerror = function (err) {
          console.log(err)
          this_.clearTimer()
        }
      },
      openMedia: function () {
        let this_ = this
        this_.imgSrc = null
        let constraints = {
          audio: false, //音频轨道
          video: true, //视频轨道
        }
        let mediaPromise = navigator.mediaDevices.getUserMedia(constraints)
        mediaPromise
          .then(function (stream) {
            this_.mediaStream = stream
            this_.srcVideo.srcObject = stream
            this_.srcVideo.play()
          })
          .catch(function (err) {
            console.log(err)
            this_.clearTimer()
          })
        this_.webcamOpen = true
      },
      takePhoto: function () {
        let canvas = document.querySelector('#canvas')
        let ctx = canvas.getContext('2d')
        ctx.drawImage(this.srcVideo, 0, 0, 1200, 900)
        this.photo.src = canvas.toDataURL()
      },
      closeMedia: function () {
        this.mediaStream.getTracks().forEach((track) => {
          track.stop()
        })
        this.clearTimer()
      },
      change: function (evt) {
        this.step = evt.target.value
      },
    },
  }
</script>
<style>
  .vertical {
    position: relative;
    top: 50%;
    transform: translateY(-50%);
  }
  .content {
    position: relative;
    top: 50%;
    transform: translateY(-50%);
    left: 50%;
    transform: translateX(-50%);
  }
  .example {
    height: 70vh;
  }

  h3 {
    font-size: 18px;
    font-family: '微软雅黑';
    font-weight: bold;
  }

  .shadow {
    box-shadow: 2px 2px 5px #000;
  }

  .dotted {
    position: relative;
    background: linear-gradient(to bottom, white, lightgray);
    width: 74%;
    height: 90%;
    margin: 0 auto;
    box-shadow: 3px 6px 5px #000;
    border-bottom: none;
  }
  .dotted-bottom {
    border-top: none;
    box-shadow: 3px 6px 5px #000;
    position: relative;
    width: 74%;
    height: 20px;
    margin: 0 auto;
    background-image: radial-gradient(
      16px at 25px 25px,
      transparent,
      transparent,
      transparent,
      transparent,
      lightgray
    );
    background-size: 50px 50px;
    background-repeat: repeat-x;
    background-position: 0px 0px;
  }
  .fix-top-right {
    position: absolute;
    top: 5px;
    right: 5px;
  }
  .settings .ant-col {
    line-height: 36px;
  }
</style>
<style lang="less">
  .icon-container {
    .ant-input-search,
    .ant-alert {
      margin-bottom: @vab-padding;
    }
    .ant-card-body {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 68px;
      cursor: pointer;

      i {
        font-size: 28px;
        text-align: center;
        pointer-events: none;
        cursor: pointer;
      }
    }
  }

  .child {
    position: absolute;
    top: 50%;
    left: 50%;
    height: 30%;
    width: 50%;
    margin: -15% 0 0 -25%;
  }
</style>
