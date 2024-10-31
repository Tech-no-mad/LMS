<template>
  <div class="book-list">
    <div v-for="(book, index) in books" :key="index" class="book-card">
      <div class="book-details">
        <h3>{{ book.title }}</h3>
        <p><strong>Author:</strong> {{ book.author }}</p>
        <div class="description-box">
          <h4>Description</h4>
          <p>{{ book.description }}</p>
        </div>
      </div>
      <button class="request-button" @click="requestBook(book.ebid, index)">Request</button>
    </div>
    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const books = ref([]);
const message = ref("");

const fetchData = async () => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.get('http://192.168.1.5:8080/api/userdashboard', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    books.value = response.data.books;
  } catch (error) {
    console.error('Error fetching books:', error);
  }
};

const requestBook = async (bookId, index) => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.post('http://192.168.1.5:8080/api/requestbook', 
      { book_id: bookId }, 
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    message.value = `Book requested successfully! Status: ${response.status}`;
    books.value.splice(index, 1);  
  } catch (error) {
    console.error('Error requesting book:', error);
    message.value = "Failed to request the book.";
  }
};


fetchData();
</script>

<style scoped>
.book-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.book-card {
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
}

.book-details {
  margin-bottom: 15px;
}

.description-box {
  margin-top: 10px;
}

.request-button {
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.request-button:hover {
  background-color: #45a049;
}

.message {
  color: #4caf50;
  font-weight: bold;
  margin-top: 20px;
}
</style>
