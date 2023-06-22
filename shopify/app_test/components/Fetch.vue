<template>
  <div class="fetch">
      <div class="fetch-title">
        Fetch
      </div>
      <div>
          <label for="start">Start date:</label>
          <input type="date" id="start" name="trip-start"
                 v-model="start_date">

          <label for="end">End date:</label>
          <input type="date" id="end" name="trip-end"
                 v-model="end_date">

          <div class="fetch-btn" @click="fetch">Fetch</div>
      </div>
      <div v-if="fetchs">
        {{fetchs}}
      </div>

  </div>
</template>

<script>
import axios from "axios";

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

export default {
    data(){
        return{
          fetchs:null,
          start_date: formatDate(new Date().setDate(new Date().getDate() - 30)),
          end_date: formatDate(new Date())
        }
    },
    components:{
    },
    methods:{
        fetch(){
            axios.post('/apps/fetch',{
                    jsonrpc:2.0,
                    params:{
                        start_date:this.start_date,
                        end_date:this.end_date
                    }
                })
                .then(response => {
                  this.fetchs = response.data
                  // this.fetchs = JSON.parse(response.data.result)
                })
                .catch(err => {
                    console.log(err)
                })
        }
    }
}
</script>

<style scoped>
    .fetch{
        margin: 60px 20% 0;
    }
    .fetch-title{
      display: flex;
        font-size: 50px;
        justify-content: center;
        font-weight: 600;
        font-style: italic;
        color: #707070;
        letter-spacing: 5px;
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
</style>