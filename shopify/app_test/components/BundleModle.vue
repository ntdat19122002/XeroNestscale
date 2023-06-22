<template>
  {{bundle}}
  <div class="bundle-modal">
    <div :style="{fontSize:bundle.font_size+'px',color:bundle.color}">{{bundle.title}}</div>
    <div>{{bundle.description}}</div>
    <div>
      <div v-for="product in bundle.products">
        <img :src="product.image" class="product-img">
        <span> x {{product.qty}}</span>
      </div>
    </div>
    <button @click="addToCart" :style="{color:bundle.color,backgroundColor:bundle.button_color}">Add bundle to cart</button>
  </div>
</template>

<script>

  import axios from "axios";

  export default {
    props:['bundle'],
    methods:{
      addToCart(){
        let items = []
        for(let product of this.bundle.products){
          items.push({
            id: product.id,
            quantity: product.qty
          })
        }
        axios.post(window.Shopify.routes.root + 'cart/add.js',{'items':items})
          .then(response => {
            window.location.href = 'https://'+window.Shopify.shop+'/cart'
          })
          .catch(err => {
              console.log(err)
          })
      }
    }
  }
</script>

<style scoped>
  .product-img{
    height: 200px;
    width: 200px;
  }
</style>