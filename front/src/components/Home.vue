<template>
  <div class="home">
    <el-container>
        <el-header>
          <h1>Smile and the world smiles with you.</h1>
        </el-header>
        <el-main>
          <el-image class="face-image" src="/face_camera" fit="fill" lazy></el-image>
          <h3 v-bind:class="messageStyle">{{message}}</h3>
        </el-main>
        <el-footer>
          <el-table stripe class="recog-table" :data="faceRecognitionList">
            <el-table-column align="center" prop="recognized_at" label="Recognized At"></el-table-column>
          </el-table>
        </el-footer>
    </el-container>
  </div>
</template>

<script>
const axios = (process.env.VUE_APP_REST_SERVER === 'json-mock')
  ? require('axios').create({ baseURL: 'http://localhost:3000' })
  : require('axios').create()
const moment = require('moment')

const RecognizePrepare = 0
const RecognizeStart = 1
const RecognizeSuccess = 2
const RecognizeFail = 3

export default {
  name: 'home',
  data () {
    return {
      rexognizeState: RecognizePrepare,
      message: "Come on simle!",
      messageStyle: "face-message-prepare",
      faceRecognitionList: []
    }
  },
  computed: {
  },
  methods: {
    setRexognizeState: function (recognizeState) {
      this.recognizeState = recognizeState

      if (this.recognizeState == RecognizePrepare) {
        this.message = "Come on simle!"
        this.messageStyle = "face-message-prepare"
      } else if (this.recognizeState == RecognizeStart) {
        this.message = "Smile more!"
        this.messageStyle = "face-message-start"
      } else if (this.recognizeState == RecognizeSuccess) {
        this.message = "Good smile!"
        this.messageStyle = "face-message-success"
      } else if (this.recognizeState == RecognizeFail) {
        this.message = "Sad face!"
        this.messageStyle = "face-message-fail"
      }
    },
    updateRecognizeFace: async function () {
      const response = await axios.get('/api/face')

      let faceRecognitionList = response.data.map(function (v) {
        const unixtime = v["recognized_at"]
        const date = moment(new Date(unixtime * 1000))
        v["recognized_at"] = date.format("YYYY/DD/MM HH:mm:ss")
        return v
      })
      faceRecognitionList.sort(function (a, b) {
        return (a["id"] > b["id"] ? -1 : 1)
      })

      this.faceRecognitionList = faceRecognitionList
    },
    getRealtimeFaceRecognition: function () {
    }
  },
  mounted () {
    this.setRexognizeState(RecognizePrepare)
    this.updateRecognizeFace()

    setInterval(function () {
      this.getRealtimeFaceRecognition()
    }, 500)
  }
}
</script>

<style scoped>
.face-image {
  width: 60%;
  margin: auto;
}
.face-message-prepare {
  color: #409EFF;
}
.face-message-start {
  color: #E6A23C;
}
.face-message-success {
  color: #67C23A;
}
.face-message-fail {
  color: #F56C6C;
}
.recog-table {
  width: 30%;
  margin: auto;
}
</style>