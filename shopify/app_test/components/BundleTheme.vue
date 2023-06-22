<template>
  <div class="bundle-theme">
    <div v-for="bundle in bundles">
      <BundleModle :bundle="bundle"/>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import BundleModle from "./BundleModle.vue";

  export default {
    components: {BundleModle},
    data(){
      return{
        bundles:[]
      }
    },
    mounted() {
      axios.post('https://odoo.website/ui/bundle', {
        jsonrpc: 2.0,
        params: {
          shop: window.Shopify.shop,
          variant: window.ShopifyAnalytics.meta.selectedVariantId
        }
      })
      .then(async (response) => {
        this.bundles = JSON.parse(response.data.result)
      })
      .catch(e => console.log(e))
    }
  }
</script>

<style scoped>

</style>