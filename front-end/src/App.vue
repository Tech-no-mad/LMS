<template>
  <NavBar v-if="showNavbar" />
  <LibNavBar v-if="libnav"></LibNavBar>
  <router-view />
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import NavBar from '@/components/Navbar.vue'; // Make sure the path is correct
import LibNavBar from './components/LibNavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar,
    LibNavBar // Registering the navbar component
  },
  setup() {
    const route = useRoute();
    const showNavbar = computed(() => {
      // Show the NavBar only if the current route's meta field 'showNavbar' is true
      return route.meta.showNavbar;
    });
    

    const libnav = computed(() => {
      // Show the NavBar only if the current route's meta field 'showNavbar' is true
      return route.meta.libnav;
    });
    return { showNavbar,libnav };
  },
  
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
