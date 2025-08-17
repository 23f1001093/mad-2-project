<template>
  <div class="container mt-5">
    <h3>Manage Chapters</h3>

    <!-- Form for adding a new chapter -->
    <form @submit.prevent="addChapter" class="mb-3 p-3 border rounded bg-light">
      <h5>Add New Chapter</h5>
      <div class="mb-3">
        <label for="newChapterName" class="form-label">Chapter Name</label>
        <input v-model="newChapterName" id="newChapterName" placeholder="Enter chapter name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="newChapterSubject" class="form-label">Subject</label>
        <select v-model="newChapterSubjectId" id="newChapterSubject" class="form-select" required>
          <option disabled value="">Please select a subject</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-success" :disabled="isSubmitting">
        {{ isSubmitting ? 'Adding...' : 'Add Chapter' }}
      </button>
    </form>

    <div v-if="loading" class="alert alert-info">
      Loading chapters and subjects...
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else>
      <div v-if="chapters.length === 0" class="alert alert-warning">
        No chapters found.
      </div>
      <div v-else>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center" v-for="chapter in chapters" :key="chapter.id">
            <span>{{ chapter.name }} ({{ getSubjectName(chapter.subject_id) }})</span>
            <div>
              <button class="btn btn-sm btn-warning me-2" @click="editChapter(chapter)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter.id)">Delete</button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Edit Chapter  -->
    <div v-if="editingChapter" class="mt-4 p-3 border rounded bg-light">
      <h4>Edit Chapter: {{ editingChapter.name }}</h4>
      <form @submit.prevent="saveChapterEdit">
        <div class="mb-3">
          <label for="editChapterName" class="form-label">Chapter Name</label>
          <input type="text" id="editChapterName" v-model="editingChapter.name" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="editChapterSubject" class="form-label">Subject</label>
          <select id="editChapterSubject" v-model="editingChapter.subject_id" class="form-select" required>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary me-2">Save Changes</button>
        <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancel</button>
      </form>
    </div>

    <div v-if="message" :class="messageClass" class="alert mt-3">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';


const API_BASE = 'http://localhost:5001';


const chapters = ref([]);
const subjects = ref([]);
const newChapterName = ref('');
const newChapterSubjectId = ref('');
const editingChapter = ref(null);
const loading = ref(true);
const isSubmitting = ref(false);
const error = ref(null);
const message = ref('');
const messageClass = ref('');


const fetchChaptersAndSubjects = async () => {
  loading.value = true;
  error.value = null;
  message.value = '';
  messageClass.value = '';
  try {
    const [chaptersRes, subjectsRes] = await Promise.all([
      fetch(`${API_BASE}/api/admin/chapters`, { credentials: 'include' }),
      fetch(`${API_BASE}/api/admin/subjects`, { credentials: 'include' })
    ]);

    if (!chaptersRes.ok) throw new Error(`Failed to fetch chapters: ${chaptersRes.statusText}`);
    if (!subjectsRes.ok) throw new Error(`Failed to fetch subjects: ${subjectsRes.statusText}`);

    chapters.value = await chaptersRes.json();
    subjects.value = await subjectsRes.json();
  } catch (err) {
    error.value = `Network error: ${err.message}`;
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// Function to get the subject name from its ID
const getSubjectName = (subjectId) => {
  const subject = subjects.value.find(s => s.id === subjectId);
  return subject ? subject.name : 'Unknown';
};

// Function to add a new chapter
const addChapter = async () => {
  isSubmitting.value = true;
  message.value = '';
  messageClass.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/admin/chapters`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ name: newChapterName.value, subject_id: newChapterSubjectId.value }),
    });
    const data = await res.json();
    if (res.ok) {
      message.value = 'Chapter added successfully!';
      messageClass.value = 'alert-success';
      newChapterName.value = '';
      newChapterSubjectId.value = '';
      await fetchChaptersAndSubjects();
    } else {
      message.value = data.message || 'Failed to add chapter.';
      messageClass.value = 'alert-danger';
    }
  } catch (err) {
    message.value = 'Network error: Could not add chapter.';
    messageClass.value = 'alert-danger';
    console.error(err);
  } finally {
    isSubmitting.value = false;
  }
};

// Function to set up the edit form with the selected chapter's data
const editChapter = (chapter) => {
  editingChapter.value = { ...chapter };
  message.value = '';
  messageClass.value = '';
};

// Function to save the changes to an edited chapter
const saveChapterEdit = async () => {
  if (!editingChapter.value) return;
  message.value = '';
  messageClass.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/admin/chapters/${editingChapter.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        name: editingChapter.value.name,
        subject_id: editingChapter.value.subject_id
      })
    });
    const data = await res.json();
    if (res.ok) {
      message.value = 'Chapter updated successfully!';
      messageClass.value = 'alert-success';
      editingChapter.value = null;
      await fetchChaptersAndSubjects();
    } else {
      message.value = data.message || 'Failed to update chapter.';
      messageClass.value = 'alert-danger';
    }
  } catch (err) {
    message.value = 'Network error updating chapter.';
    messageClass.value = 'alert-danger';
    console.error(err);
  }
};

// Function to close the edit form
const cancelEdit = () => {
  editingChapter.value = null;
  message.value = '';
  messageClass.value = '';
};

// Function to delete a chapter
const deleteChapter = async (id) => {
  if (!confirm('Are you sure you want to delete this chapter? This cannot be undone.')) {
    return;
  }
  message.value = '';
  messageClass.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/admin/chapters/${id}`, {
      method: 'DELETE',
      credentials: 'include',
    });
    const data = await res.json();
    if (res.ok) {
      message.value = 'Chapter deleted successfully!';
      messageClass.value = 'alert-success';
      await fetchChaptersAndSubjects();
    } else {
      message.value = data.message || 'Failed to delete chapter.';
      messageClass.value = 'alert-danger';
    }
  } catch (err) {
    message.value = 'Network error deleting chapter.';
    messageClass.value = 'alert-danger';
    console.error(err);
  }
};


onMounted(fetchChaptersAndSubjects);
</script>

<style scoped>

</style>
