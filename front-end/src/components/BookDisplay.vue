<template>
    <div class="book-display">
        <div v-for="(section, index) in sections" :key="index" class="section-card">
            <div v-for="book in computedBooksForSection(section.sid)" :key="book.ebid" class="book-card">
                <h3>{{ book.title }}</h3>
                <p>{{ book.author }}</p>
                <button class="edit-button" @click="editBook(book)">Edit Book</button>
                <button class="delete-button" @click="deleteBook(book)">Delete Book</button>
            </div>
        </div>
    </div>
  </template>
  
  <script>
 
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  import axios from 'axios';

  export default {
    name: 'BookDisplay',
    
    setup() {
      const store = useStore();
       const router = useRouter()
       const sections = store.state.sections 
      // Get the books associated with the section ID
      const computedBooksForSection = (sectionId) => {
      console.log(store.state.books)
      return store.getters.getBooksForSection(sectionId);
    };
  
      function editBook(book) {
        // Handle edit book logic
        console.log('Editing book:', book);
        router.push({name:'edit-book'})
      }
  
      async function deleteBook(book,section) {
      console.log("SECTION ID TO DELETE", section.sid, section.description);
      console.log("BOOK ID TO DELETE", book.ebid, book.description);

      try {
        const response = await axios.delete('http://192.168.1.5:8080/api/delete-section', {
          data: section,book,
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${sessionStorage.getItem('token')}`,
          },
        });

        store.commit('SET_SECTIONS', response.data.sections);
        console.log('Sections updated in store');
        router.push({ name: 'LibDash' });
      } catch (error) {
        console.error('Error deleting section:', error);
        // Handle the error gracefully, e.g., display an error message to the user
      }
    }
  
      return {
      
        editBook,
        deleteBook,
        computedBooksForSection,
        sections
      };
    },
  };
  </script>
  
  <style scoped>
.book-display {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; /* Adjust spacing between book cards */
}

.book-card {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 12px;
  width: 200px; /* Set desired card width */
}

.edit-button,
.delete-button {
  background-color: #0074d9;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  margin-right: 8px;
}
</style>