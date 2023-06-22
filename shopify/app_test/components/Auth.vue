<template>
  <div class="auth">
      <div class="auth-item">
        <i class="fa-solid fa-user"></i>
      </div>
      <div @click="logout" class="auth-item">
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
  .auth{
    display: flex;
  }
  .auth-item{
      font-size: 20px;
      padding: 10px 30px;
      cursor: pointer;
  }
  a{
      color:white !important;
  }
  i{
    display: flex;
    align-items: center;
  }
</style>