<template>
  <div>
    <el-container>
        <el-header>
          <h1 v-bind:class="messageStyle">{{message}}</h1>
        </el-header>
        <el-main>
          <el-image class="face-image" v-bind:src="faceImage" fit="fill" lazy></el-image>
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
const isDebug = (process.env.VUE_APP_REST_SERVER === 'json-mock')
const axios = isDebug
  ? require('axios').create({ baseURL: 'http://localhost:3000' })
  : require('axios').create()
const moment = require('moment')
const lena = require('../assets/lena.png')

const FaceRecogState = new Object({
  noFace: 0,
  detectFace: 1,
  detectSmile: 2,
  success: 3,
  fail: 4
})

export default {
  name: 'home',
  data () {
    return {
      state: FaceRecogState.noFace,
      message: "Come on simle!",
      messageStyle: "message-prepare",
      lastList: [],
      faceImage: isDebug ? lena : "/face/camera",
      updateStateTimer: null
    }
  },
  computed: {
  },
  methods: {
    updateLastList: async function () {
      try {
        const response = await axios.get('/api/face/list')

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
      } catch (error) {
        console.log(error)
      }
    },
    setState: function (state) {
      this.state = state

      if (this.state === FaceRecogState.noFace) {
        this.message = "Show your face!"
        this.messageStyle = "message-no"
      } else if (this.state === FaceRecogState.detectFace) {
        this.message = "Come on simle!"
        this.messageStyle = "message-face"
      } else if (this.state === FaceRecogState.detectSmile) {
        this.message = "Smile more!"
        this.messageStyle = "message-smile"
      } else if (this.state === FaceRecogState.success) {
        this.message = "Good smile!"
        this.messageStyle = "message-success"
        
        this.updateLastList()
      } else if (this.state === FaceRecogState.fail) {
        this.message = "Sad face!"
        this.messageStyle = "message-fail"
      }
    },
    getState: async function () {
      try {
        const response = await axios.get('/api/face/state')
        const state = response.data["state"]
        this.setState(state)
      } catch (error) {
        console.log(error)
      }
    },
    setTimer: function () {
      if (this.updateStateTimer === null) {
        this.updateStateTimer = setInterval(() => {
          this.getState()
        }, 1000)
      }
    }
  },
  mounted () {
    this.setState(FaceRecogState.noFace)
    this.updateLastList()
    this.setTimer()
  },
  updated () {
    this.setTimer()
  },
  destroyed () {
    if (this.updateStateTimer) {
      clearInterval(this.updateStateTimer)
    }
  }
}
</script>

<style scoped>
.face-image {
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 10px;
}
.message-no {
  color: #409EFF;
}
.message-face {
  color: #409EFF;
}
.message-smile {
  color: #E6A23C;
}
.message-success {
  color: #67C23A;
}
.message-fail {
  color: #F56C6C;
}
.recog-table {
  max-width: 200px;
  width: auto;
  margin: auto;
}
</style>