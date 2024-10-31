// store.js
import {createStore} from 'vuex';

const store = createStore({
  state() {
    return {
      sections: [],
      objSection:null // Your initial state (empty array for sections)
    };
  },
  mutations: {
    SET_SECTIONS(state, sections) {
      state.sections = sections;
    },
  },
  actions: {
    setSections({ commit }, sections) {
      commit('SET_SECTIONS', sections);
    },
  },
});

export default store;
