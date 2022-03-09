<template>
  <div class="example">
    <a-spin
      class="content"
      :spinning="!imgShow"
      size="large"
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
        <a-card
          title="点餐详情"
          :bordered="true"
          style="width: 450px; margin-left: 50px"
          :style="{ height: height + 'px' }"
        >
          <div :style="{ height: height - 150 + 'px' }">
            <span v-if="step == 1" class="vertical">请放入菜品...</span>
            <span v-if="step == 2" class="vertical">
              <a-spin :spinning="step == 2" size="large" tip="正在识别..." />
            </span>
            <div v-if="step == 3" class="dotted">
              <a-divider dashed style="width: 50%">合并订单</a-divider>
              <div class="vertical">
                <p v-for="(v, i) in currOrder.items" :key="i">
                  {{ v.type }}
                  {{ v.unit }}x
                  {{ v.count }}
                </p>
                <a-divider dashed />
                <div>合计:¥{{ currOrder.sum }}</div>
              </div>
            </div>
            <div v-if="step == 3" class="dotted-bottom"></div>
          </div>
          <a-row type="flex" v-if="step == 3">
            <a-col flex="auto" style="text-align: center">
              <a-button type="primary">重新识别</a-button>
            </a-col>
            <a-col flex="auto" style="text-align: center">
              <a-button type="primary">模拟支付</a-button>
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
  export default {
    name: 'Index',
    data() {
      return {
        step: 2, // 1 识别区为空等待放入 2 识别中  3 识别完成待支付
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
        fps: 200,
        currOrder: null,
        plates: [],
        accumulator: 0,
        detectCount: 10,
      }
    },
    mounted() {
      this.initSource()
      this.createWebSocket()
    },
    unmounted() {
      this.closeMedia()
    },
    methods: {
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
            this_.videoImg = canvas.toDataURL('image/jpeg', 0.3)
            var data = this_.videoImg.split(',')
            this_.ws.send(data[1])
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
        } else {
          this.step = 2
        }

        if (this.step == 2) {
          this.imgShow = true
          this.imgSrc = this_.prefix + data.image
          if (JSON.stringify(this.plates) == JSON.stringify(data.plates)) {
            this.accumulator++
            console.log(this.step, this.accumulator)
          } else {
            this.accumulator = 0
          }
          this.plates = data.plates
          if (this.accumulator > this.detectCount) {
            this.step = 3
            this.clearTimer()
            this.createOrder()
          }
        }
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
        }
        for (const key in currOrder) {
          console.log(key)
          const e = currOrder[key]
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

  .dotted {
    position: relative;
    background: linear-gradient(to bottom, white, lightgray);
    width: 74%;
    height: 90%;
    margin: 0 auto;
  }
  .dotted-bottom {
    position: relative;
    width: 74%;
    height: 20px;
    margin: 0 auto;
    background: white;
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
</style>
