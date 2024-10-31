<template>
  <div class="card">
    <h2>Edit Section</h2>
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
      <button type="submit" class="edit-section-button">Edit Section</button>
    </form>
  </div>
</template>


<script setup>
import {  computed } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

console.log(store.state.objSection)
// Initialize computed properties with Vuex state values
const title = computed({
  get: () => store.state.objSection.title,
  set: (value) => (store.state.objSection.title = value),
});

const dateCreated = computed({
  get: () => store.state.objSection.date,
  set: (value) => (store.state.objSection.date = value),
});

const description = computed({
  get: () => store.state.objSection.description,
  set: (value) => (store.state.objSection.description = value),
});

const submitForm = () => {
  // Logic for editing a section (unchanged)
  axios
    .post(
      'http://192.168.1.5:8080/api/edit-section',
      {
        title: title.value,
        date: dateCreated.value,
        description: description.value,
        sid: store.state.objSection.sid,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${sessionStorage.getItem('token')}`, // Your JWT token
        },
      }
    )
    .then((response) => {
      console.log('Section edited successfully:', response.data);
      
      store.state.sections = response.data.sections;
      router.push({ name: 'LibDash' });
    })
    .catch((error) => {
      console.error('Error editing section:', error);
      
    });

    return {
        title,
        description,
        dateCreated,
        submitForm,
      };  
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



.edit-section-button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #5cb85c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.edit-section-button:hover {
  background-color: #4cae4c;
}


</style>