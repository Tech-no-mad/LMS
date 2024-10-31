<template>
  <div class="navbar">
    <nav>
      <ul>
        <li @click="goToDashboard">User's Dashboard</li>
        <li @click="MyBooks">MyBooks</li>
        <li class="active">Books</li>
        <li>Stats</li>
        <li @click="logout">Logout</li>
        <li @click="goToStart" class="back-button">Back</li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default {
  name: 'nav-bar',
  setup() {
    const router = useRouter();
    const jwtToken = ref(sessionStorage.getItem('jwtToken'));

    const goToDashboard = () => {
      router.push('/user-dashboard');
    };

    const MyBooks = () => {
      router.push('/my-books');
    };

    const logout = () => {
      jwtToken.value = null;
      localStorage.removeItem('jwtToken');
      router.push('/user-login');
    };
    const goToStart = () => {
      router.push('/');
    };

    return {
      goToDashboard,
      MyBooks,
      logout,
      goToStart
    };
  },
};
</script>

<style scoped>
.navbar {
  background-color: #39814d;
  padding: 10px 0;
}

nav ul {
  list-style-type: none;
  display: flex;
  justify-content: space-around;
}

nav li {
  padding: 10px;
  border-right: 1px solid #ccc;
  cursor: pointer;
}

nav li:last-child {
  border-right: none;
}

nav li a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

nav li.active {
  background-color: lightblue;
  border-radius: 5px;
  color: white;
}
</style>
