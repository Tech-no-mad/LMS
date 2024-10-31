<template>
  <div class="requests-page">
    <div class="search-filter">
      <input v-model="searchQuery" placeholder="Search requests" @input="filterRequests" class="search-input" />
      <button @click="toggleFilter" class="filter-button">Filter</button>
    </div>
    <div class="request-list">
      <h3>Pending Requests</h3>
      <div v-for="request in filteredRequests" :key="request.id" class="request-card" @click="selectRequest(request)">
        <div class="request-details">
          <p><strong>Book Title:</strong> {{ request.book_title }}</p>
          <p><strong>User:</strong> {{ request.user_name }}</p>
        </div>
        <div class="request-actions">
          <button @click.stop="grantRequest(request.id)" class="grant-button">Grant</button>
          <button @click.stop="rejectRequest(request.id)" class="reject-button">Reject</button>
        </div>
      </div>
    </div>

    <div class="granted-list">
      <h3>Granted Requests</h3>
      <div v-for="request in grantedRequests" :key="request.id" class="request-card">
        <div class="request-details">
          <p><strong>Book Title:</strong> {{ request.book_title }}</p>
          <p><strong>User:</strong> {{ request.user_name }}</p>
        </div>
        <div class="request-actions">
          <button @click.stop="revokeRequest(request.id)" class="revoke-button">Revoke</button>
        </div>
      </div>
    </div>

    <div class="returned-list">
      <h3>Returned Books</h3>
      <div v-for="request in returnedRequests" :key="request.id" class="request-card">
        <div class="request-details">
          <p><strong>Book Title:</strong> {{ request.book_title }}</p>
          <p><strong>User:</strong> {{ request.user_name }}</p>
        </div>
        <div class="request-actions">
          <button @click="viewBook(request.pdf)" class="view-button">View Book</button>
        </div>
      </div>
    </div>

    <!-- Modal Popup -->
    <div v-if="selectedRequest" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-details">
          <p><strong>Username:</strong> {{ selectedRequest.user_name }}</p>
          <p><strong>Days Requested:</strong> {{ selectedRequest.days_requested }}</p>
          <p><strong>Book Title:</strong> {{ selectedRequest.book_title }}</p>
          <p><strong>Book Section:</strong> {{ selectedRequest.book_section }}</p>
        </div>
        <div class="modal-actions">
          <button @click="rejectRequest(selectedRequest.id)" class="reject-button">Reject</button>
          <button @click="grantRequest(selectedRequest.id)" class="grant-button">Grant</button>
          <button @click="viewBook(selectedRequest.pdf)" class="view-button">View Book</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const requests = ref([]);
const searchQuery = ref('');
const filteredRequests = ref([]);
const grantedRequests = ref([]);
const returnedRequests = ref([]);
const showFilter = ref(false);
const selectedRequest = ref(null);

const fetchRequests = async () => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.get('http://192.168.1.5:8080/api/getrequests', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    requests.value = response.data.requests;
    filteredRequests.value = requests.value.filter(request => request.status === 'request'); // Initial filter for current requests
    grantedRequests.value = requests.value.filter(request => request.status === 'grant'); // Filter for granted requests
    returnedRequests.value = requests.value.filter(request => request.status === 'return'); // Filter for returned requests
  } catch (error) {
    console.error('Error fetching requests:', error);
  }
};

const filterRequests = () => {
  if (searchQuery.value) {
    filteredRequests.value = requests.value.filter(request =>
      request.book_title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      request.user_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  } else {
    filteredRequests.value = requests.value.filter(request => request.status === 'current'); // Exclude granted and returned requests
  }
};

const toggleFilter = () => {
  showFilter.value = !showFilter.value;
  // Implement your filter logic here
};

const grantRequest = async (requestId) => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.post(`http://192.168.1.5:8080/api/grantrequest/${requestId}`, 
    { transaction_id: requestId }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.status === 200) {
      const request = requests.value.find(r => r.id === requestId);
      if (request) {
        request.status = 'grant';
        grantedRequests.value.push(request);
        filteredRequests.value = filteredRequests.value.filter(r => r.id !== requestId);
      }
    }
  } catch (error) {
    console.error('Error granting request:', error);
  }
};

const rejectRequest = async (requestId) => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.delete(`http://192.168.1.5:8080/api/rejectrequest/${requestId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) {
      filteredRequests.value = filteredRequests.value.filter(r => r.id !== requestId);
      requests.value = requests.value.filter(r => r.id !== requestId);
    }
  } catch (error) {
    console.error('Error rejecting request:', error);
  }
};

const revokeRequest = async (requestId) => {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.delete(`http://192.168.1.5:8080/api/rejectrequest/${requestId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) {
      grantedRequests.value = grantedRequests.value.filter(r => r.id !== requestId);
      requests.value = requests.value.filter(r => r.id !== requestId);
      filteredRequests.value = filteredRequests.value.filter(r => r.id !== requestId);
    }
  } catch (error) {
    console.error('Error revoking request:', error);
  }
};

const viewBook = async (pdf) => {
  const backendUrl = `http://192.168.1.5:8080${pdf}`;
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
      window.open(url, '_blank');
    } else {
      console.error('Failed to fetch PDF:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching PDF:', error);
  }
};

const selectRequest = (request) => {
  selectedRequest.value = request;
};

const closeModal = () => {
  selectedRequest.value = null;
};

onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
.requests-page {
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

.request-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.request-card {
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

.request-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.request-details p {
  margin: 0;
  color: #333;
}

.request-actions {
  display: flex;
  gap: 10px;
}

.grant-button, .reject-button, .view-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.grant-button {
  background-color: #28a745;
  color: white;
}

.grant-button:hover {
  background-color: #218838;
}

.reject-button {
  background-color: #dc3545;
  color: white;
}

.reject-button:hover {
  background-color: #c82333;
}

.view-button {
  background-color: #ffc107;
  color: white;
}

.view-button:hover {
  background-color: #e0a800;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal-details p {
  margin: 10px 0;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}
</style>
