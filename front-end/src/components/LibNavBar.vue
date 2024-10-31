<template>
  <div class="librarian-navbar">
    <nav>
      <ul>
        <li class="active" @click="goToLibDash">Librarian's Dashboard</li>
        <li class="active" @click="getbooks">Manage Books</li>
        <li class="active" @click="goToRequests">Requests</li>
        <li class="active" @click="genreport">Reports</li>
        <li class="active" @click="lendings">Lendings</li>
        <li class="active" @click="logout">Logout</li>
        <li @click="goToStart" class="back-button">Back</li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
export default {
  name: 'lib-nav-bar',
  setup() {
    const store = useStore(); // Get the Vuex store
    const router = useRouter();

    const goToLibDash = () => {
      console.log(store.state.sections);
      router.push({ name: 'LibDash' });
    };

    const getbooks = () => {
      console.log(store.state.sections);
      console.log(store.state.books);
      router.push({ name: 'display-book' });
    };

    const goToRequests = () => {
      router.push({ name: 'requests-page' });
    };

    const logout = () => {
      sessionStorage.removeItem('token');
      router.push({ name: 'librarian-login' });
    };

    const genreport = () => {
      router.push({ name: 'report-all' });
    };

    const lendings = () =>{
      router.push({name : 'user-lendings'})
    }
    const goToStart = () => {
      router.push('/');
    };

    return {
      goToLibDash,
      getbooks,
      goToRequests,
      genreport,
      logout,
      lendings,
      goToStart
    };
  },
};
</script>

<style scoped>
.librarian-navbar {
  background-color: #6c757d; /* A different shade for the librarian navbar */
  padding: 10px 0;
}

nav ul {
  list-style-type: none;
  display: flex;
  justify-content: space-around;
}

nav li {
  padding: 10px;
  border-right: 1px solid #ddd; /* A lighter border color */
}

nav li:last-child {
  border-right: none;
}

nav li a {
  text-decoration: none;
  color: #f8f9fa; /* A light color for text */
  font-weight: bold;
}

nav li.active {
  background-color: #007bff; /* A different active color */
  border-radius: 5px;
  color: white;
}
</style>
