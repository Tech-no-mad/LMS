<template>
    <div class="card">
      <h2>Add New Section</h2>
      <form @submit.prevent="submitForm" class="form">
        <div class="form-group">
          <label for="section-title">Title:</label>
          <input type="text" id="section-title" v-model="title" required />
        </div>
        <div class="form-group">
          <label for="section-date">Date Created:</label>
          <input type="date" id="section-date" v-model="dateCreated" required />
        </div>
        <div class="form-group">
          <label for="section-description">Description:</label>
          <textarea id="section-description" v-model="description" required></textarea>
        </div>
        <button type="submit" class="add-section-button">Add Section</button>
      </form>
    </div>
  </template>

    <script>
    import axios from 'axios';
    //import { useStore } from 'vuex';

    //import jwt_decode from 'jsonwebtoken'
    export default {
    name: 'SectionAdd',
    // setup(){
    //     const store = useStore();
    // },
    data() {
    return {
    
    jwtToken: sessionStorage.getItem('token'),
    title: '',
    dateCreated: '',
    description: ''
    };
    },
    methods: {
    submitForm() {
        console.log(this.sectionData)
       
    // Logic for adding a new section
    axios.post('http://192.168.1.5:8080/api/add_section', 
    {
        title: this.title,
        dateCreated: this.dateCreated,
        description: this.description,
    },
    {
    //withCredentials: true,
    headers: {
    Authorization: `Bearer ${this.jwtToken}`, // Your JWT token
    },
    }) 
    .then(response => {
    console.log('Section added successfully:', response.data);
    const addedSections = response.data.sections; // Extract the sections
    this.$store.dispatch('setSections', addedSections);

    this.$router.push({name:'LibDash'})
    })
    .catch(error => {
    console.error('Error adding section:', error.response.data);
    // Handle the error (e.g., show an error message)
    });
    },
  
    },
    };
    </script>



<style scoped>
.card {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
}

.form-group input[type="text"],
.form-group input[type="date"],
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-section-button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #5cb85c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-section-button:hover {
  background-color: #4cae4c;
}
</style>