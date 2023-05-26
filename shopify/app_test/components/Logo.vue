<template>
  <div @click="getHomePage" class="logo">
      Shopify xero
  </div>
</template>

<script>
export default {
  methods:{
      getHomePage(){
          this.$store.commit('changeRoute','/apps/shopify')
      }
  }
}
</script>

<style scoped>
  .logo{
      margin: auto;
      padding: 0 10px;
      font-weight: 600;
      font-size: 35px;
      font-style: italic;
      color: white !important;
      cursor: pointer;
  }

</style>