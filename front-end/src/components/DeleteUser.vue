<template>
    <div class="delete-user-container">
      <h2>Delete User</h2>
      <form @submit.prevent="deleteUser">
        <div class="input-group">
          <label for="userId">User ID</label>
          <input type="text" id="userId" v-model="userId" placeholder="Enter User ID" />
        </div>
        <button type="submit" class="delete-user-button">Delete</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'DeleteUser',
    data() {
      return {
        userId: '',
      };
    },
    methods: {
        deleteUser() 
        {
        axios.delete(`http://192.168.1.5:8080/api/users/${this.userId}`)
          .then(response => {
            console.log('User deleted:', response.data);
            // Handle further logic like redirecting or displaying a success message
            this.$router.push({name:'user-login'})
          })
          .catch(error => {
            console.error('Error deleting user:', error.response.data);
            // Handle errors, such as displaying an error message to the user
          });
    }
  }
  }
  </script>
  
  <style scoped>
  .delete-user-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  .input-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .input-group input {
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .delete-user-button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #ff4d4d;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .delete-user-button:hover {
    background-color: #ff3333;
  }
  </style>
  
  