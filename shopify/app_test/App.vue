<template>
    <Header/>
    <div v-if="url == 'https://odoo.website/apps/shopify'">
        <Home/>
    </div>
    <div v-else-if="url == 'https://odoo.website/apps/shopify/integration'">
        <Integrations/>
    </div>
    <div v-else-if="url == 'https://odoo.website/apps/shopify/fetch'">
        <Fetch/>
    </div>
    <div v-else-if="url == 'https://odoo.website/apps/shopify/xero'">
        <Xero/>
    </div>
    <div v-else-if="url == 'https://odoo.website/apps/shopify/bundle'">
        <Bundle/>
    </div>
    <div v-else-if="url == 'https://odoo.website/apps/shopify/analytic'">
        <Analytic/>
    </div>
    <div v-else>
        The page is not found
    </div>
</template>

<script>

import Header from "./components/Header.vue";
import Integrations from "./components/Integrations.vue";
import Fetch from "./components/Fetch.vue";
import Home from "./components/Home.vue";
import Xero from "./components/Xero.vue";
import Analytic from "./components/Analytic.vue";
import Bundle from "./components/Bundle.vue";

export default {
    name: "App",
    components: {Bundle, Xero, Home, Fetch, Integrations, Header, Analytic},
    computed: {
        url(){
            return this.$store.state.url
        }
    }
}
</script>

<style src="./css/main.css"></style>