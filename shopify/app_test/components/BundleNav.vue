<template>
  <div class="bundle-nav">
    <div class="bundle-nav-item" @click="getPage('bundle')">Bundle</div>
    <div class="bundle-nav-item" @click="getPage('product')">Product</div>
  </div>
</template>

<script>
  export default {
    data(){
      return {

      }
    },
    methods:{
        getPage(nav){
            this.$store.commit('changeRoute',`/apps/shopify/${nav}`)
        }
    },
  }
</script>

<style scoped>
  .bundle-nav{
    width: 245px;
    background: #8bdd8b;
    height: 88vh;
  }

  .bundle-nav-item{
    width: 100%;
    padding: 30px;
    color: white;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
  }
  .bundle-nav-item:hover{
    background: #16c016;
  }
</style>