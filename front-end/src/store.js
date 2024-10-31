// store.js
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      sections: [],
      books: [],
      objSection: null,
      objBook:null,
      sid:null 
    };
  },
  mutations: {
    SET_SECTIONS(state, sections) {
      state.sections = sections;
    },
    SET_BOOKS(state, books) {
      state.books = books;
    },
  },
  actions: {
    setSections({ commit }, sections) {
      commit('SET_SECTIONS', sections);
    },
    setBooks({ commit }, books) {
      commit('SET_BOOKS', books);
    },
  },
  getters: {
    // Define a getter to return the sections array
    getSections(state) {
      return state.sections;
    },
    // Define a getter to retrieve books associated with a specific section
    getBooksForSection: (state) => (sectionId) => {
      return state.books.filter((book) => book.sectionid === sectionId);
    },
  },
});

export default store;
