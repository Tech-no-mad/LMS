<template>
    <div class="user-actions">
      <button class="delete-button" @click="deleteUser">Delete</button>
      <button class="update-button" @click="updateUser">Update</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name : 'dummy-comp',
    data() {
      return {
        jwtToken: sessionStorage.getItem('token'), // JWT token
        userId: 1 // Replace with dynamic user ID if needed
      };
    },
    methods: {
      deleteUser() {
        axios.delete(`http://192.168.1.5:8080/api/users/${this.userId}`, {
          headers: {
            'Authorization': `Bearer ${this.jwtToken}`
          }
        })
        .then(response => {
          console.log('User deleted:', response.data);
          // Redirect or show a message
        })
        .catch(error => {
          console.error('Error deleting user:', error);
          // Show an error message
        });
      },
      updateUser() {
        this.$router.push({name:'UpdateUser'})
      }
    }
  }
  </script>
  
  <style scoped>
  .user-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
  }
  
  .delete-button, .update-button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .delete-button {
    background-color: #ff4d4f;
    color: white;
  }
  
  .update-button {
    background-color: #4caf50;
    color: white;
  }
  </style>
  