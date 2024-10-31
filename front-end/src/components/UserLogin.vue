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
        <!-- <button type="button" @click.prevent="deleteuser" class="del-button">Delete User</button>
        <button type="button" @click.prevent="updateuser" class="update-button">Update User</button> -->
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
    login() {
      const credentials = {
        username: this.username,
        password: this.password
        // role: this.selectedRole, // Ensure 'selectedRole' is defined in data if you're using it
      };
      console.log('username :',credentials.username);
      axios.post('http://192.168.1.5:8080/api/login', {
                  username: this.username,
                  password: this.password
      },
      {
        withCredentials: true
      })
     .then(response => {
  // Handle success
          console.log(response.data);
         sessionStorage.setItem('token', response.data.access_token);
          this.$router.push({name : 'user-dashboard'})
      })
     .catch(error => {
  // Handle error
          console.log('Login failed:', error.response.data);
      });
    },
    register() {
      // Navigate to the userreg.vue component
      this.$router.push({ name: 'UserReg' });
    },
    deleteuser()
    {
      this.$router.push({ name: 'DeleteUser' });
    },
    updateuser()
    {
      this.$router.push({ name: 'UpdateUser' });
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
  .register-button,
  .del-button,
  .update-button {
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

.del-button {
  background-color: red;
  color: #000;
}

.update-button {
  background-color: green;
  color: #000;
}
  </style>
  