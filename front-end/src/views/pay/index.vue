<template>
  <div class="example">
    <a-spin
      class="content"
      :spinning="!imgShow"
      size="large"
      tip="拼命加载中..."
    />
    <a-row type="flex" v-show="imgShow">
      <a-col flex="100px">
        <div>
          <img
            :src="imgSrc"
            :width="width"
            :height="height"
            id="photo"
            @load="onload"
          />
        </div>
        <video
          v-show="!imgShow"
          id="video"
          class="src-video"
          :width="width"
          :height="height"
          autoplay="autoplay"
        ></video>
      </a-col>
      <a-col flex="auto" style="text-align:center">
        <a-card title="点餐详情" :bordered="false" style="width: 300px">
          <a-button type="primary">重新识别</a-button>
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
        this.height = h * 0.79
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
            var data = canvas.toDataURL('image/jpeg', 0.3).split(',')
            this_.ws.send(data[1])
          }
        }, this_.fps)
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
          this_.imgSrc = this_.prefix + evt.data
        }
        this.ws.onclose = function () {
          console.log('Closed')
        }
        this.ws.onerror = function (err) {
          alert('Error: ' + err)
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
            alert(err)
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
    },
  }
</script>
<style>
  .content {
    position: relative;
    top: 50%;
    transform: translateY(-50%);
    left: 50%;
    transform: translateX(-50%);
  }
  .example {
    height: 80vh;
  }
</style>
