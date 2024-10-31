<template>
  <div class="my-books">
    <div class="search-filter">
      <input v-model="searchQuery" placeholder="Search" @input="filterBooks" />
      <button @click="toggleFilter">Filter</button>
    </div>

    <div class="books-section">
      <h3>Current</h3>
      <div class="book-list">
        <div v-for="book in filteredCurrentBooks" :key="book.id" class="book-card">
          <div class="book-info">
            <p><strong>{{ book.title }}</strong> | {{ book.author }} | {{ book.section }}</p>
          </div>
          <button class="return-button" @click="returnBook(book.id)">Return</button>
          <button class="download-button" @click="downloadPDF(book.pdf)">Download Book</button>
        </div>
      </div>
    </div>

    <div class="books-section">
      <h3>Completed</h3>
      <div class="book-list">
        <div v-for="book in filteredCompletedBooks" :key="book.id" class="book-card">
          <div class="book-info">
            <p><strong>{{ book.title }}</strong> | {{ book.author }} | {{ book.section }}</p>
          </div>
          <button class="rating-button" @click="rateBook(book.id)">Rate</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const searchQuery = ref('');

const currentBooks = ref([]);
const completedBooks = ref([]);
const filteredCurrentBooks = ref([]);
const filteredCompletedBooks = ref([]);
const showFilter = ref(false);

const fetchBooks = async () => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.get('http://192.168.1.5:8080/api/mybooks', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Separate books based on their statuses
    currentBooks.value = response.data.current_books.filter(book => book.status === 'grant');
    completedBooks.value = response.data.completed_books.filter(book => book.status === 'return');

    filteredCurrentBooks.value = currentBooks.value;
    filteredCompletedBooks.value = completedBooks.value;
  } catch (error) {
    console.error('Error fetching books:', error);
  }
};

const filterBooks = () => {
  if (searchQuery.value) {
    filteredCurrentBooks.value = currentBooks.value.filter(book =>
      book.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
    filteredCompletedBooks.value = completedBooks.value.filter(book =>
      book.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  } else {
    filteredCurrentBooks.value = currentBooks.value;
    filteredCompletedBooks.value = completedBooks.value;
  }
};

const toggleFilter = () => {
  showFilter.value = !showFilter.value;
};

const returnBook = async (bookId) => {
  try {
    const token = sessionStorage.getItem('token');
    await axios.post(
      'http://192.168.1.5:8080/api/returnbook',
      { book_id: bookId },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    fetchBooks(); // Refresh the list of books after returning
  } catch (error) {
    console.error('Error returning book:', error);
  }
};

const rateBook = async (bookId) => {
  const rating = prompt("Please enter your rating for this book (1-5):");
  if (rating < 1 || rating > 5) {
    alert("Rating should be between 1 and 5.");
    return;
  }

  try {
    const token = sessionStorage.getItem('token');
    await axios.post(
      'http://192.168.1.5:8080/api/addrating',
      { book_id: bookId, rating },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    alert("Rating submitted successfully!");
  } catch (error) {
    console.error('Error submitting rating:', error);
  }
};


const downloadPDF = async (downloadPDF) => {
  const backendUrl = `http://192.168.1.5:8080${downloadPDF}`;
  try {
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
      },
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'book.pdf');  
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      console.error('Failed to download PDF:', response.statusText);
    }
  } catch (error) {
    console.error('Error downloading PDF:', error);
  }
};



onMounted(() => {
  fetchBooks();
});
</script>

<style scoped>
.my-books {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-filter {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  padding: 10px;
  width: 70%;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.filter-button {
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.filter-button:hover {
  background-color: #0056b3;
}

.books-section {
  margin-bottom: 30px;
}

.book-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.book-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.book-info p {
  margin: 0;
  color: #333;
}

.return-button, .rating-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.return-button {
  background-color: #28a745;
  color: white;
}

.return-button:hover {
  background-color: #218838;
}

.rating-button {
  background-color: #ffc107;
  color: white;
}

.rating-button:hover {
  background-color: #e0a800;
}

.download-button {
  background-color: #28a745;
  color: white; 
}

.download-button:hover {
  background-color: #218838; 
}
</style>
