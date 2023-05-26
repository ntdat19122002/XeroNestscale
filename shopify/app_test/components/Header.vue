<template>
    <div className="header">
        <div className="header-left">
            <Logo/>
            <Navbar/>
        </div>
        <div className="header-right">
            <Auth/>
        </div>
    </div>
</template>

<script>
import Logo from './Logo.vue'
import Navbar from './Navbar.vue'
import Auth from "./Auth.vue";

export default {
    components: {Auth, Logo, Navbar},

}
</script>

<style>
.header {
    position: relative;
    width: 100vw;
    height: 100px;
    padding: 0 20px;
    background: green;
    display: flex;
    justify-content: space-between;
    color: white;
    align-items: center;
    z-index: 10;
}

.header-left{
    display: flex;
    height: 100%;
}
</style>