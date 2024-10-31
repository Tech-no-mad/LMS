<template>
  <div class="add-book-form">
    <h2>Add a New Book</h2>
    <form @submit.prevent="submitForm">
      <label for="title">Title:</label>
      <input type="text" id="title" v-model="title" required>

      <label for="author">Author:</label>
      <input type="text" id="author" v-model="author" required>

      <label for="content">Content:</label>
      <textarea id="content" v-model="description"></textarea>

      <label for="date">Date:</label>
      <input type="date" id="date" v-model="date" required>

      <label for="filelink">Ebook Link:</label>
      <input type="file" id = "filelink" @change="fileUpload"  accept=".pdf, .doc" />

      <label for="quantity">Quantity:</label>
      <input type="number" id="quantity" v-model="quantity" required>

      <label for="price">Price:</label>
      <input type="number" id="price" v-model="price" required>

      <label for="section">Section:</label>
      <input type="text" id="section" v-model="section" disabled>

      <button type="submit">Add Book</button>
    </form>
  </div>
</template>

<script>
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ref,computed } from 'vue';

export default {
  name: 'BookAdd',
  setup() {
    const store = useStore();
    const router = useRouter();
    //const jwtToken = sessionStorage.getItem('token');

    const title = ref('');
    const description = ref('');
    const author = ref('');
    const date = ref('');
    const filelink = ref(null)
    const price = ref(0)
    const quantity = ref(0)
    const section = computed({
        get: () => store.state.objSection.title        
      // Add a set function if needed
    });


    const fileUpload = (event) => {

      filelink.value = event.target.files[0]
      console.log(filelink.value)
};


    const submitForm = () => {
      console.log('Adding a new book...');
      const formData = new FormData(); 
      formData.append('file', filelink.value);
      formData.append('title', title.value);
      formData.append('author', author.value);
      formData.append('description', description.value);
      formData.append('date', date.value);
      formData.append('sid', store.state.objSection.sid);
      formData.append('quantity', quantity.value);
      formData.append('price', price.value);
      console.log(formData)
      axios
        .post(
          'http://192.168.1.5:8080/api/add_book',formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${sessionStorage.getItem('token')}`,
            },
          }
        )
        .then((response) => {
          console.log('Book added successfully:', response.data);
          store.state.sections = response.data.sections
          store.commit('SET_BOOKS', response.data.books);
          router.push({ name: 'LibDash' });
        })
        .catch((error) => {
          console.error('Error adding book:', error.response.data);
          
        });
    };

    return {
      title,
      description,
      author,
      section,
      date,
      submitForm,
      quantity,
      price,
      fileUpload
    };
  },
};
</script>

<style scoped>
.add-book-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.add-book-form h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.add-book-form label {
  display: block;
  margin-bottom: 10px;
}

.add-book-form input,
.add-book-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.add-book-form button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
}

.add-book-form button:hover {
  background-color: #0056b3;
}

/* Book Card Styles */
.book-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  transition: transform 0.2s ease;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.book-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.book-card p {
  font-size: 14px;
  color: #555;
}

/* Optional: Add more styles as needed (e.g., image, buttons, etc.) */


</style>