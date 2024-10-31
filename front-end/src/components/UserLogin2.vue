<template>
    <div class="login-container">
      <h2>User Login</h2>
      <form @submit.prevent="login">
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="User_01" />
        </div>
  
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" />
        </div>
  
        
  
        <button type="submit" class="login-button">Login</button>
        <button type="button" @click.prevent="register" class="register-button">Register</button>
      </form>
    </div>
  </template>
  
  <script>
import axios from 'axios'
export default {
  name: 'user-login',
  data() {
    return {
      username: '',
      password: '',
      // role: this.selectedRole, // This line might also cause an error because 'this' is not available in data()
    };
  },
  methods: {
//     login() {
//   const params = new URLSearchParams();
//   params.append('username', this.username);
//   params.append('password', this.password);

//   axios.post('http://192.168.0.161:8080/api/login', params)
//     .then(response => {
//       // Handle success
//       console.log(response.data);
//     })
//     .catch(error => {
//       // Handle error
//       if (error.response) {
//         console.log('Login failed:', error.response.data);
//       } else {
//         console.log('Login failed:', error.message);
//       }
//     });
// }

login(){

    const data = {
  param1: 'value1',
  param2: 'value2'
};

axios.post('http://192.168.0.161:8080/api/login', data)
  .then(response => {
    // handle success
    console.log(response.data);
  })
  .catch(error => {
    // handle error
    console.error(error);
  });



}

  }
}
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
  
  .login-button,
  .register-button {
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
  