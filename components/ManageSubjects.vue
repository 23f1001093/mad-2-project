<template>
  <div class="container mt-5">
    <h3>Manage Subjects</h3>

    <form @submit.prevent="addSubject" class="mb-3 d-flex">
      <input v-model="newSubject" placeholder="New Subject" class="form-control me-2" required />
      <button type="submit" class="btn btn-success">Add</button>
    </form>

    <div v-if="subjects.length > 0">
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center" v-for="subject in subjects" :key="subject.id">
          <span>{{ subject.name }}</span>
          <div>
            <button class="btn btn-sm btn-warning me-2" @click="editSubject(subject)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteSubject(subject.id)">Delete</button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="text-muted">No subjects available.</div>

    <div v-if="message" :class="messageClass" class="alert mt-3">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const subjects = ref([]);
const newSubject = ref('');
const message = ref('');
const messageClass = ref('');

const API_BASE = 'http://localhost:5001'; // Define API_BASE for consistency

const loadSubjects = async () => {
  message.value = ''; // Clear previous messages
  messageClass.value = '';
  try {
    // CORRECTED: URL to /api/admin/subjects
    const res = await fetch(`${API_BASE}/api/admin/subjects`, { credentials: 'include' });
    if (res.ok) {
      subjects.value = await res.json();
    } else {
      const errorData = await res.json().catch(() => ({ message: 'Failed to load subjects.' }));
      message.value = errorData.message || `Error: ${res.status} when loading subjects.`;
      messageClass.value = 'alert-danger';
      subjects.value = []; // Clear subjects on error
    }
  } catch (error) {
    console.error('Network or parsing error:', error);
    message.value = 'Network error: Could not connect to the server.';
    messageClass.value = 'alert-danger';
    subjects.value = [];
  }
};

const addSubject = async () => {
  message.value = ''; // Clear previous messages
  messageClass.value = '';
  try {
    // CORRECTED: URL to /api/admin/subjects
    const res = await fetch(`${API_BASE}/api/admin/subjects`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newSubject.value }),
    });
    const data = await res.json();
    if (res.ok) {
      newSubject.value = '';
      message.value = 'Subject added successfully!';
      messageClass.value = 'alert-success';
      await loadSubjects();
    } else {
      message.value = data.message || 'Failed to add subject.';
      messageClass.value = 'alert-danger';
    }
  } catch (error) {
    console.error('Network or parsing error:', error);
    message.value = 'Network error: Could not add subject.';
    messageClass.value = 'alert-danger';
  }
};

const editSubject = async (subject) => {
  message.value = ''; // Clear previous messages
  messageClass.value = '';
  const name = prompt('Enter new name:', subject.name);
  if (name && name !== subject.name) {
    try {
      // CORRECTED: URL to /api/admin/subjects/${subject.id}
      const res = await fetch(`${API_BASE}/api/admin/subjects/${subject.id}`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
      });
      const data = await res.json();
      if (res.ok) {
        message.value = 'Subject updated successfully!';
        messageClass.value = 'alert-success';
        await loadSubjects();
      } else {
        message.value = data.message || 'Failed to update subject.';
        messageClass.value = 'alert-danger';
      }
    } catch (error) {
      console.error('Network or parsing error:', error);
      message.value = 'Network error: Could not update subject.';
      messageClass.value = 'alert-danger';
    }
  }
};

const deleteSubject = async (id) => {
  message.value = ''; // Clear previous messages
  messageClass.value = '';
  if (confirm('Are you sure you want to delete this subject?')) {
    try {
      // CORRECTED: URL to /api/admin/subjects/${id}
      const res = await fetch(`${API_BASE}/api/admin/subjects/${id}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      const data = await res.json();
      if (res.ok) {
        message.value = 'Subject deleted successfully!';
        messageClass.value = 'alert-success';
        await loadSubjects();
      } else {
        message.value = data.message || 'Failed to delete subject.';
        messageClass.value = 'alert-danger';
      }
    } catch (error) {
      console.error('Network or parsing error:', error);
      message.value = 'Network error: Could not delete subject.';
      messageClass.value = 'alert-danger';
    }
  }
};

onMounted(loadSubjects);
</script>