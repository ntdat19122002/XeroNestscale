<template>
  <div class="auth">
      <div @click="logout" class="logout">
          Logout
      </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  methods:{
      logout(){
          window.location.href = '/web/session/logout'
      }
  }
}
</script>

<style>
  .logout{
      font-size: 20px;
      padding: 10px 30px;
      cursor: pointer;
  }
  a{
      color:white !important;
  }
</style>