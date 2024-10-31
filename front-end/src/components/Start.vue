<template>
    <div class="role-selection">
      <h2>Select your role:</h2>
      <button @click="routeTo('user')">User</button>
      <button @click="routeTo('librarian')">Librarian</button>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'start-page',
    setup() {
      const router = useRouter();
      return { router };
    },
    methods: {
      routeTo(role) {
        if (role === 'user') {
          this.router.push({ name: 'user-login' });
        } else if (role === 'librarian') {
          this.router.push({ name: 'librarian-login' });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .role-selection {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .role-selection button {
    margin: 10px;
    padding: 10px 20px;
    font-size: 16px;
    color: white;
    background-color: #5c6bc0; /* Attractive blue shade */
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .role-selection button:hover {
    background-color: #3949ab; /* Darker shade on hover */
  }
  </style>
  