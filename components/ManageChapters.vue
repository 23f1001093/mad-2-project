<template>
  <div class="container mt-5">
    <h2>Manage Chapters</h2>
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
      <table v-else class="table table-striped">
        <thead>
          <tr>
            <th>Chapter Name</th>
            <th>Subject</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="chapter in chapters" :key="chapter.id">
            <td>{{ chapter.name }}</td>
            <td>{{ getSubjectName(chapter.subject_id) }}</td>
            <td>
              <!-- The Edit button that was missing -->
              <button class="btn btn-sm btn-warning me-2" @click="editChapter(chapter)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Chapter Form (only visible when editingChapter is set) -->
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

    <div v-if="message" class="alert mt-3" :class="messageClass">
      {{ message }}
    </div>
  </div>
</template>

<script>
// Assuming API_BASE is correctly imported from a separate file
import { API_BASE } from '../api';

export default {
  name: "ManageChapters",
  data() {
    return {
      chapters: [],
      subjects: [],
      editingChapter: null,
      loading: true,
      error: null,
      message: '',
      messageClass: '',
    };
  },
  methods: {
    // Fetches all chapters from the API
    async fetchChapters() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters`, { credentials: 'include' });
        if (response.ok) {
          this.chapters = await response.json();
        } else {
          this.error = `Failed to fetch chapters: ${response.statusText}`;
          console.error(this.error);
        }
      } catch (err) {
        this.error = 'Network error fetching chapters.';
        console.error(this.error, err);
      }
    },
    // Fetches all subjects for the dropdown list in the edit form
    async fetchSubjects() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/subjects`, { credentials: 'include' });
        if (response.ok) {
          this.subjects = await response.json();
        } else {
          this.error = `Failed to fetch subjects: ${response.statusText}`;
          console.error(this.error);
        }
      } catch (err) {
        this.error = 'Network error fetching subjects.';
        console.error(this.error, err);
      } finally {
        this.loading = false;
      }
    },
    // Finds the subject name from the list of subjects based on subject_id
    getSubjectName(subjectId) {
      const subject = this.subjects.find(s => s.id === subjectId);
      return subject ? subject.name : 'Unknown';
    },
    // Populates the form with the selected chapter's data
    editChapter(chapter) {
      this.editingChapter = { ...chapter };
      this.message = '';
      this.messageClass = '';
    },
    // Makes the API call to save the edited chapter
    async saveChapterEdit() {
      if (!this.editingChapter) return;
      this.message = '';
      this.messageClass = '';
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters/${this.editingChapter.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.editingChapter)
        });
        const data = await response.json();
        if (response.ok) {
          this.message = data.message || 'Chapter updated successfully!';
          this.messageClass = 'alert-success';
          this.editingChapter = null; // Close the edit form
          this.fetchChapters(); // Refresh the list
        } else {
          this.message = `Failed to update chapter: ${data.message || response.statusText}`;
          this.messageClass = 'alert-danger';
          console.error('Error updating chapter:', data);
        }
      } catch (err) {
        this.message = 'Network error updating chapter.';
        this.messageClass = 'alert-danger';
        console.error('Network error updating chapter:', err);
      }
    },
    // Closes the edit form without saving
    cancelEdit() {
      this.editingChapter = null;
      this.message = '';
      this.messageClass = '';
    },
    // Makes the API call to delete a chapter
    async deleteChapter(chapterId) {
      if (!confirm('Are you sure you want to delete this chapter? This will also delete any associated quizzes and questions.')) {
        return;
      }
      this.message = '';
      this.messageClass = '';
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters/${chapterId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        const data = await response.json();
        if (response.ok) {
          this.message = data.message || 'Chapter deleted successfully!';
          this.messageClass = 'alert-success';
          this.chapters = this.chapters.filter(c => c.id !== chapterId);
        } else {
          this.message = `Failed to delete chapter: ${data.message || response.statusText}`;
          this.messageClass = 'alert-danger';
          console.error('Error deleting chapter:', data);
        }
      } catch (err) {
        this.message = 'Network error deleting chapter.';
        this.messageClass = 'alert-danger';
        console.error('Network error deleting chapter:', err);
      }
    }
  },
  mounted() {
    // Fetch both chapters and subjects on component load
    Promise.all([this.fetchChapters(), this.fetchSubjects()]);
  },
};
</script>
