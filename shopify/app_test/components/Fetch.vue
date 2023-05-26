<template>
  <div class="fetch">
      <div>
          <label for="start">Start date:</label>
          <input type="date" id="start" name="trip-start"
                 value="2018-07-22">

          <label for="end">End date:</label>
          <input type="date" id="end" name="trip-start"
                 value="2018-07-22">

          <div class="fetch-btn" @click="fetch">Fetch</div>
      </div>
      <div v-for="fetch in fetchs[0]">
          {{fetch}}
      </div>
  </div>
</template>

<script>
import axios from "axios";
import {DateRangePickerComponent} from "@syncfusion/ej2-vue-calendars";

export default {
    data(){
        return{
          fetchs:[]
        }
    },
    components:{
    },
    methods:{
        fetch(){
            axios.post('/apps/fetch',{
                    jsonrpc:2.0,
                    params:{}
                })
                .then(reponse => this.fetchs = reponse.data)
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