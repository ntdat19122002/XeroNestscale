<template>
    <div class="navbar">
        <div v-for="nav in navlist" @click="getPage(nav)" class="navbar-item">
            {{ nav.charAt(0).toUpperCase() + nav.slice(1) }}
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            navlist: ['fetch', 'integration', 'xero', 'bundle', 'analytic']
        }
    },
    methods:{
        getPage(nav){
            this.$store.commit('changeRoute',`/apps/shopify/${nav}`)
        }
    },
    computed: {
        count () {
          return this.$store.state.count
        }
    }
}
</script>

<style>
  .navbar{
      display: flex;
      padding: 0 87px;
  }
  .navbar-item{
      padding: 0 35px;
      letter-spacing: 2px;
      font-weight: 700;
      display: flex;
      align-items: center;
      cursor: pointer;
      transform: skewX(-20deg);
  }
  .navbar-item:hover{
      background: #007000;
  }
</style>