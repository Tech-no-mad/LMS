<template>
    <div class="update-user-container">
      <h2>Update User</h2>
      <form @submit.prevent="updateUser">
        <div class="input-group">
          <label for="userId">User ID</label>
          <input type="text" id="userId" v-model="userId" placeholder="Enter User ID" />
        </div>
        <div class="input-group">
          <label for="username">New Username</label>
          <input type="text" id="username" v-model="username" placeholder="New Username" />
        </div>
        <div class="input-group">
          <label for="email">New Email</label>
          <input type="email" id="email" v-model="email" placeholder="New Email" />
        </div>
        <button type="submit" class="update-user-button">Update</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UpdateUser',
    data() {
      return {
        userId: '',
        username: '',
        email: '',
        jwtToken: sessionStorage.getItem('access_token'), // JWT token
      };
    },
    methods: {
        updateUser() 
        {
        const userData = {
            username: this.username,
            email: this.email
        };
        axios.put(`http://192.168.1.5:8080/api/update_user/${this.userId}`, userData, { 
          withCredentials: true,
          headers: {
            'Authorization': `Bearer ${this.jwtToken}`
          }
          
        })
            .then(response => {
            console.log('User updated:', response.data);
            // Handle further logic like redirecting or displaying a success message
            })
            .catch(error => {
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.error('Error updating user:', error.response.data);
            } else if (error.request) {
                // The request was made but no response was received
                console.error('Error updating user: No response received', error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.error('Error:', error.message);
            }
            // Log the entire error object for debugging
           
            console.log(this.jwtToken);
            });
        }

    }
  }
  </script>
  
  <style scoped>
  .update-user-container {
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
  
  .update-user-button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #4CAF50; /* A green color for the update button */
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .update-user-button:hover {
    background-color: #45a049; /* A darker green color on hover */
  }
  </style>
  