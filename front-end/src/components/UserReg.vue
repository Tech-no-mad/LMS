<template>
  <div class="register-container">
    <h2>User Registration</h2>
    <form @submit.prevent="register">
      <div class="input-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" placeholder="User_01" required />
      </div>

      <div class="input-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>

      <div class="input-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" placeholder="user@example.com" required />
      </div>

      <button type="submit" class="register-button">Register</button>
      <!-- Display the message here -->
      <p v-if="message">{{ message }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
  name: 'user-reg',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      message: '' // This will hold the success or error message
    };
  },
  methods: {
    async register() {
      try {
        const registrationData = {
          username: this.username,
          password: this.password,
          email: this.email
        };
        const response = await axios.post('http://192.168.0.161:8080/api/register', registrationData, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.data.msg === "User created successfully") {
          sessionStorage.setItem('access_token', response.data.access_token);
            console.log("inserted data")
            this.message = 'Registered successfully!'; // Update the success message
          // this.$router.push('/dashboard'); // Uncomment if using Vue Router
            this.$router.push({name:'user-login'})
        }   
        else {

              this.message = 'Registration failed';
        }
      } 
      catch (error) 
      {
        // Check if the error response exists and has a data property with a message
        if (error.response && error.response.data && error.response.data.msg) {
          this.message = error.response.data.msg;
        } else {
          // If the error response does not have a data property with a message, use a generic error message
          this.message = 'An unexpected error occurred. Please try again later.';
        }
        console.error('Registration Error:', error); // Log the error to the console for debugging
      }

    }
  }
};
</script>

  <style scoped>
  .register-container {
    max-width: 300px;
    margin: auto;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .input-group {
    margin-bottom: 10px;
  }
  
  .input-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .input-group input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .register-button {
    width: 100%;
    padding: 10px;
    background-color: #5cb85c; /* Green */
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .register-button:hover {
    background-color: #4cae4c; /* Darker green */
  }
  </style>
  
  
  
  