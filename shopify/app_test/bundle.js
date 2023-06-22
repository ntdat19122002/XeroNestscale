import {createApp, h} from 'vue/dist/vue.esm-bundler';
import 'ant-design-vue/dist/antd.css';
import BundleTheme from "./components/BundleTheme.vue";



var app_bundle = createApp({
    name: 'AppBundle',
    render: () => {
        return <BundleTheme/>
    }
})

app_bundle.mount('#app-bundle-id')