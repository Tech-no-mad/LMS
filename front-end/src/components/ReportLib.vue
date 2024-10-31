<template>
  <div class="report-box" id="myreport" >
    <div class="container-fluid">
      <div class="report-summary">
        <h2>Report on {{ formattedDate }}</h2>
        <hr class="separator">
        <div class="summary-left">
          <h2>Total Sections: {{ sections.length }}</h2>
        </div>
        <div class="summary-right">
          <h2>Total Books: {{ books.length }}</h2>
        </div>
        
      </div>
      <hr class="separator"> <!-- Horizontal line to separate summary and sections -->
      <div v-for="(section, index) in sections" :key="index">
        <h2>Section Title: {{ section.title }}</h2>
        <hr class="separator"> <!-- Horizontal line to separate sections -->
        <table class="book-table">
          <thead>
            <tr>
              <th class="table-header">Book Title</th>
              <th class="table-header">Book Author</th>
              <th class="table-header">Book Description</th>
              <th class="table-header">Book Price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in getBooksForSection(section.sid)" :key="book.ebid">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>{{ book.description }}</td>
              <td>{{ book.price }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <button @click="generatePDF" class="generate-button">Generate PDF</button>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import jsPDF from 'jspdf';
import domtoimage from 'dom-to-image';

const store = useStore();

// Get sections and books from the store
const sections = computed(() => store.state.sections);
const books = computed(() => store.state.books)
const getBooksForSection = (sectionId) => store.getters.getBooksForSection(sectionId);
const today = new Date()
const formattedDate = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;

const generatePDF = async () => {
  const pdf = new jsPDF('l', 'pt', 'a4');
  const element = document.getElementById('myreport'); 
  console.log(element)
  try {
    const imageData = await domtoimage.toPng(element);
    pdf.addImage(imageData, 'PNG', 0, 0, pdf.internal.pageSize.getWidth(), pdf.internal.pageSize.getHeight());
    pdf.save('my-report.pdf');
  } catch (error) {
    console.error('Error generating PDF:', error);
  }

  return{
    formattedDate,
    generatePDF,
   
  }
};

</script>

<style scoped>
.report-box {
  border: 1px solid #ccc;
  padding: 1rem;
}

.container-fluid {
  width: 100%;
}

.report-summary {
  width: 100%;
  margin-bottom: 1rem;
}

.separator {
  border-top: 1px solid #ccc;
  margin: 1rem 0;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  text-align: center;
  background-color: #f2f2f2;
  border: 1px solid #ccc;
  padding: 8px;
}

.book-table td {
  border: 1px solid #ccc;
  padding: 8px;
}

.summary-left {
  float: left;
  width: 48%;
}

.summary-right {
  float: right;
  width: 48%;
}

.generate-button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: block;
  margin: 20px auto; /* Center the button */
}

</style>
