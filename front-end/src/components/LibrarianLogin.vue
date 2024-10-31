<template>
    <div class="login-container">
      <h2>Librarian Login</h2>
      <form ref="loginForm" @submit.prevent="login" class="form">
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="Lib_01" />
        </div>
  
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" />
        </div>          
        <button type="submit" class="login-button">Login</button>
        
      </form>
    </div>
  </template>
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  //import router from '@/router/index.js';
  
  const store = useStore();
  const router = useRouter();
  const username = ref('');
  const password = ref('');
  const selectedRole = ref('librarian'); // Initialize with the appropriate default value
  
  const login = async () => {
  try {
    const credentials = {
      username: username.value,
      password: password.value,
      role: selectedRole.value,
    };

    const response = await axios.post('http://192.168.1.5:8080/api/liblogin', credentials);
    console.log('Response data:', response.data);
    sessionStorage.setItem('token', response.data.access_token);
    store.state.sections = response.data.sections;
    console.log('store sections:', store.state.sections);
    store.state.books = response.data.books;
    console.log('store books:', store.state.books);
    router.push({ name: 'LibDash' });
  } catch (error) {
    // Handle error (e.g., show error message)
    console.error('Login failed:', error.response); // Example: { message: 'Invalid username or password' }
  }
};

  </script>
  
  <style scoped>  
  .login-container {
    max-width: 400px;
    margin: auto;
  }
  
  .input-group {
    margin-bottom: 15px;
  
    label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
    }
  
    input[type='text'],
    input[type='password'],
    select {
      width: calc(100% - 20px);
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
  }
  
  .login-button {
    padding: 10px;
    border: none; 
    cursor: pointer;
    border-radius: 5px;
    color: #fff;
    width: 100%;

  }
  .login-button {
  background-color: rgb(33, 38, 190);
}

.register-button {
  background-color: yellow;
  color: #000;
}
  </style>
  