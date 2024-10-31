<template>
  <div class="dashboard">
    <div class="header">
      <h1>Library Dashboard</h1>
      <button class="add-section" @click="addNewSection">+</button>
    </div>

    <input
      type="text"
      v-model="searchSec"
      name = "searchSec"
      placeholder="Search for sections and presss enter"
      @change="handleInput('searchSec')"
      class="search-bar"
    />   

    <input
      type="text"
      v-model="searchBook"
      name="searchBook"
      placeholder="Search for books and presss enter"
      @change="handleInput('searchBook')"
      class="search-bar"
    />

    <div class="content">
      <p v-if="filteredSections.length === 0">No matching sections or books found.</p>

      <div v-if ="searchBook.length === 0" class = 'section-card'>

        <div v-for="(section, index) in filteredSections" :key="index" class="section-card">
          <h2 class="section-title">Section:{{ section.title }}</h2>
          <p class="section-content">Section Content:{{ section.description }}</p>

          <div v-for=  "book in computedBooksForSection(section.sid)" :key="book.ebid" class="book-card">
              <h3>Book:{{ book.title }}</h3>
              <p>Author:{{ book.author }}</p>
              <p>Description:{{ book.description }}</p>
              <p>EBook Link:{{ book.file}}</p>
              <button class="edit-button-book" @click="editBook(book)">Edit Book</button>
              <button  class="delete-button-book" @click="deleteBook(book)">Delete Book</button>
          </div>
          <button class="edit-button-section" @click="editSection(section)">Edit Section</button>
          <button  class="delete-button-section " @click="deleteSection(section)">Delete Section</button>
          <button  class="add-button-section " @click="addNewSection(section)">AddSection</button>
          <button class="add-book-button" @click="addBook(section)">Add Book</button>
        </div>

      </div> 

        <div v-if="searchSec.length === 0" class = 'section-card'> 
          <div v-for = "book in filteredBooks" :key="book.ebid" class="book-card">
              <h3>Book:{{ book.title }}</h3>
              <p>Author:{{ book.author }}</p>
              <p>Description:{{ book.description }}</p>
              <button class="edit-button-book" @click="editBook(book)">Edit Book</button>
              <button  class="delete-button-book" @click="deleteBook(book)">Delete Book</button>
          </div>
        </div>

     
      
    </div>
  </div>

    
</template>

<script>
import { ref,computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';

export default {
  name: 'lib-dash',
  setup() {
    const router = useRouter();
    const store = useStore();
    const sections = ref([]);
    const books = ref([]);
    const searchSec = ref('');
    const searchBook = ref('');
    const files = ref([])

    sections.value = store.state.sections;
    books.value = store.state.books
    console.log('books'+books.value)

    
    const handleFileUpload = (event) => {

    files.value = Array.from(event.target.files);
 
};

    const handleInput = (field) =>{
      if (field === 'searchSec') {
        searchBook.value = '';
        const sbook = document.querySelector('[name="searchBook"]').focus();
        if (sbook) {
      sbook.focus(); 
    }
      } else if (field === 'searchBook') {
        searchSec.value = ''; 
        const ssec = document.querySelector('[name="searchSec"]').focus(); 
        if (ssec) {
      ssec.focus(); 
    }
      }
      console.log(field)
    }

const submitFile = async () => {
  try {
    const formData = new FormData();
    files.value.forEach((file) => {
        formData.append('files', file);
      });
    const response = await axios.post('http://192.168.1.5:8080/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', 
        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
      },
    });

    console.log(response.data);
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};


    const filteredSections = computed(() => {
      return sections.value.filter((section) =>
        section.title.toLowerCase().includes(searchSec.value.toLowerCase())
      );
    });

    const filteredBooks = computed(() => {
      return books.value.filter((book) =>
          book.title.toLowerCase().includes(searchBook.value.toLowerCase())
        ) 
  });
    const computedBooksForSection = (sectionId) => {
      console.log(store.state.books)
      return store.getters.getBooksForSection(sectionId);
    };

    function addNewSection() {
      router.push({ name: 'add-section' });
    }

    function editSection(section) {
      console.log("SECTION ID TO EDIT ", section.sid, section.description);
      console.log(section)
      // Commit a mutation to update the section in the store
      store.state.objSection = section
      router.push({ name: 'edit-section' });
    }

    function editBook(book) {
      console.log("BOOK  ID TO EDIT ", book.ebid, book.description);
      // Commit a mutation to update the section in the store
      
      store.state.objBook = book
      router.push({ name: 'edit-book' });
    }

    async function deleteSection(section) {
      console.log("SECTION ID TO DELETE", section.sid, section.description);
     
      try {
        const response = await axios.delete('http://192.168.1.5:8080/api/delete-section', {
          data: section,
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${sessionStorage.getItem('token')}`,
          },
        });

        store.commit('SET_SECTIONS', response.data.sections);
        store.commit('SET_BOOKS',response.data.books)
        console.log('Sections updated in store');
        router.push({ name: 'LibDash' });
      } catch (error) {
        console.error('Error deleting section:', error);
        // Handle the error gracefully, e.g., display an error message to the user
      }
    }

    async function deleteBook(book) {
     
      console.log("BOOK ID TO DELETE", book.ebid);

      try {                     
        const response = await axios.delete('http://192.168.1.5:8080/api/delete_book', {
          data: book,
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${sessionStorage.getItem('token')}`,
          },
        });

        store.commit('SET_SECTIONS', response.data.sections);
        store.commit('SET_BOOKS',response.data.books)
        console.log('Sections updated in store');
        router.push({ name: 'LibDash' });
      } catch (error) {
        console.error('Error deleting book:', error);
        // Handle the error gracefully, e.g., display an error message to the user
      }
    }

    function addBook(section) {
      console.log(section.sid);
      store.state.objSection = section;
      router.push({ name: 'add-book' });
    }

   

    return {
      sections,
      addNewSection,
      editSection,
      deleteSection,
      addBook,
      computedBooksForSection,
      editBook,
      deleteBook,
      searchSec,
      searchBook,
      filteredSections,
      filteredBooks,
      handleFileUpload,
      handleInput,
      submitFile
    };
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.add-section {
  background-color: #0074d9;
  color: #fff;
  border: none;
  border-radius: 50%;
  padding: 8px;
  cursor: pointer;
  font-size: 18px;
}

.content {
  margin-top: 20px;
}

.section-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px; /* Adjust spacing between section cards */
}

.section-card {
  flex: 1;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 20px;
  margin: 0;
}

.section-content {
  font-size: 14px;
  color: #555;
}


.book-card {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 12px;
  margin-top: 10px;
}

.edit-button-book,
.edit-button-section {
  background-color: #0074d9;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  margin-right: 8px;
  cursor: pointer;
}

.delete-button-book,
.delete-button-section {
  background-color: #ff4136;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
}

.add-book-button {
  background-color: #2ecc40;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
}

.add-button-section {
  background-color: #06b1e6;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
}

.search-bar {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 1rem;
}

</style>