<template>
  <div class="xero">
      <div class="check-connect">
          <span v-if="connected">
              Connected
          </span>
      </div>
      <button @click="connectXero" class="connect-xero-btn">Connect Xero</button>
      <div class="xero-fetch">
          <label for="start">Start date:</label>
          <input type="date" id="start" name="trip-start"
                 value="2018-07-22">

          <label for="end">End date:</label>
          <input type="date" id="end" name="trip-start"
                 value="2018-07-22">

          <div class="fetch-btn" @click="fetch">Fetch</div>
      </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
    data(){
        return{
            connected: false
        }
    },
    methods:{
        connectXero(){
            axios.get('/xero/auth2',)
              .then(response => console.log('ok'))
              .catch(err => console.log(err.response.data))
        }
    },
    mounted() {
      axios.get('/xero/check_connected')
          .then(respose => this.connected = respose.data['check'])
          .catch(err => console.log(err))
    }
}
</script>

<style scoped>
  .connect-xero-btn{
      float: right;
      margin-top: -142px;
      margin-right: 20%;
      padding: 10px;
      border-color: #d7c2c2;
      color: #502020;
      background: #f3dddd;
  }

  input[type="date"] {
      width: 30%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 3px;
      font-size: 14px;
    }

    label {
        font-weight: bold;
        display: block;
        font: 1rem 'Fira Sans', sans-serif;
    }

    input,
    label {
        margin: 0.4rem 0;
    }

    .fetch-btn{
        font-weight: 900;
        width: fit-content;
        color: white;
        display: block;
        padding: 8px 16px;
        cursor: pointer;
        background: #95de59;
        border-radius: 40px;
    }

    .check-connect{
        border: 10px green solid;
        background: #9af59a;
        width: fit-content;
        border-radius: 50%;
        padding: 118px;
        transform: translate(-50%, -51%);
    }

    .check-connect span{
        font-style: italic;
        color: white;
        font-size: 20px;
        top: 150px;
        font-weight: 600;
        left: -34px;
        position: absolute;
        transform: translateX(154px);
    }

    .xero-fetch{
        margin : -50px 20% 0;
    }
</style>