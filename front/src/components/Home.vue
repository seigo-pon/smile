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
          <el-table stripe class="recog-table" :data="lastList">
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

const FaceRecognitionStatePrepare = 0
const FaceRecognitionStateStart = 1
const FaceRecognitionStateSuccess = 2
const FaceRecognitionStateFail = 3

export default {
  name: 'home',
  data () {
    return {
      state: FaceRecognitionStatePrepare,
      message: "Come on simle!",
      messageStyle: "message-prepare",
      lastList: []
    }
  },
  computed: {
  },
  methods: {
    setRecognitionState: function (recognizeState) {
      this.state = recognizeState

      if (this.state == FaceRecognitionStatePrepare) {
        this.message = "Come on simle!"
        this.messageStyle = "message-prepare"
      } else if (this.state == FaceRecognitionStateStart) {
        this.message = "Smile more!"
        this.messageStyle = "message-start"
      } else if (this.state == FaceRecognitionStateSuccess) {
        this.message = "Good smile!"
        this.messageStyle = "message-success"
      } else if (this.state == FaceRecognitionStateFail) {
        this.message = "Sad face!"
        this.messageStyle = "message-fail"
      }
    },
    updateLastList: async function () {
      const response = await axios.get('/api/last_list')

      let list = response.data.map(function (v) {
        const unixtime = v["recognized_at"]
        const date = moment(new Date(unixtime * 1000))
        v["recognized_at"] = date.format("YYYY/DD/MM HH:mm:ss")
        return v
      })
      list.sort(function (a, b) {
        return (a["id"] > b["id"] ? -1 : 1)
      })

      this.lastList = list
    },
    getCurrentRecognitionState: async function () {
      const response = await axios.get('/api/state')
      const state = response.data
      console.log(state)
      this.setRecognitionState(state)
    }
  },
  mounted () {
    this.setRecognitionState(FaceRecognitionStatePrepare)
    this.updateLastList()
    
    setInterval(() => {
      this.getCurrentRecognitionState()
    }, 500)
  }
}
</script>

<style scoped>
.face-image {
  width: 60%;
  margin: auto;
}
.message-prepare {
  color: #409EFF;
}
.message-start {
  color: #E6A23C;
}
.message-success {
  color: #67C23A;
}
.message-fail {
  color: #F56C6C;
}
.recog-table {
  width: 30%;
  margin: auto;
}
</style>