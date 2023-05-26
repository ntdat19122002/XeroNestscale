<template>
  <div class="bundle">
      {{visible}}
      <div>
          Discount rule:
      </div>
      <select>
          <option>%</option>
          <option>Fix amount</option>
      </select>
      <div>
          Product
           <Button type="primary" @click="showModal">Open Modal</Button>
            <Modal v-model:visible="visible" title="Basic Modal" @ok="handleOk">
              <p>Some contents...</p>
              <p>Some contents...</p>
              <p>Some contents...</p>
            </Modal>
          <div>
              Quantity
              <input type="number"/>
          </div>
      </div>
  </div>
</template>

<script>
    import { Modal,Button } from "ant-design-vue";
    import { defineComponent, ref } from 'vue';
    export default {
        data(){
            return{
                visible:false
            }
        },
        components: {
          Modal,
          Button,
      },
        methods:{
            showModal(){
                this.visible = true
            },
            handleOk(e){
              console.log(e);
              this.visible = false;
            }
        }
    }
</script>

<style scoped>
  .bundle{
      margin: 20px 20%;
  }
</style>