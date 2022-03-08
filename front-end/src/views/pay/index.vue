<template>
  <div>
    <!-- <button onclick="openMedia()">开启摄像头</button>
    <button onclick="closeMedia()">关闭摄像头</button>
    <button onclick="takePhoto()">拍照</button> -->
    <video
      id="video"
      style="position: float; display: none;"
      class="src-video"
      :width="width"
      :height="height"
      autoplay="autoplay"
    ></video>
    <canvas
      id="canvas"
      style="display: none;"
      :width="width"
      :height="height"
    ></canvas>
    <div v-if="imgSrc">
      <img :src="imgSrc" :width="width" :height="height" id="photo" />
    </div>
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
        fps: 200,
      }
    },
    mounted() {
      this.clearTimer()
      this.initSource()
      this.createWebSocket()
      this.openMedia()
      this.createTimer()
    },
    unmounted(){
       this.closeMedia()
    },
    methods: {
      initSource: function () {
        this.srcVideo = document.getElementById('video')
        this.photo = document.getElementById('photo')
        let h = document.body.clientHeight
        let w = document.body.clientWidth
        this.width=w*0.5
        this.height=h*0.79
        console.log(h, w)
      },
      clearTimer: function () {
        if (this.timer) {
          clearTimeout(this.timer)
          console.log("Timer 已清除")
        }
      },
      createTimer: function () {
        let this_ = this
        this.timer = setInterval(function () {
          if (this_.webcamOpen) {
            let canvas = document.getElementById('canvas')
            let ctx = canvas.getContext('2d')
            ctx.drawImage(this_.srcVideo, 0, 0, 1200, 900)
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
            /* 使用这个stream stream */
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
