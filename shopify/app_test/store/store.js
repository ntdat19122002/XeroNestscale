import {createStore} from "vuex";

export const store = createStore({
  state () {
    return {
      url: window.location.href,
      count: 0
    }
  },
  mutations: {
    increment (state) {
      state.count++
    },
    changeRoute (state,url_change){
      state.url = 'https://odoo.website'+url_change
      history.pushState({}, "", url_change);
    }
  }
})