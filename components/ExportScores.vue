<template>
  <div class="container mt-5">
    <h2>Export Quiz Scores</h2>
    <div class="card p-4">
      <h4 class="card-title">Select a Quiz to Export Scores</h4>
      <div class="mb-3">
        <label for="quizSelect" class="form-label">Quiz</label>
        <select id="quizSelect" v-model="selectedQuizId" class="form-select" required>
          <option disabled value="">Please select a quiz</option>
          <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
            {{ quiz.name }} - {{ getChapterName(quiz.chapter_id) }}
          </option>
        </select>
      </div>
      <div class="mb-3">
        <button @click="exportScores" class="btn btn-primary" :disabled="!selectedQuizId || loading">
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          {{ loading ? 'Exporting...' : 'Export Scores for Selected Quiz' }}
        </button>
      </div>
      <div v-if="message" class="alert mt-3" :class="messageClass" role="alert">
        {{ message }}
      </div>
      <div v-if="downloadLink" class="mt-3">
        <a :href="downloadLink" download class="btn btn-success">Download Exported Scores</a>
      </div>
    </div>
  </div>
</template>

<script>
import { API_BASE } from '../api';

export default {
  name: "ExportScores",
  data() {
    return {
      quizzes: [],
      chapters: [],
      selectedQuizId: '',
      loading: false,
      message: '',
      messageClass: '',
      downloadLink: null,
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes`, { credentials: 'include' });
        if (response.ok) {
          const data = await response.json();
          this.quizzes = data.quizzes || [];
        } else {
          console.error('Error fetching quizzes:', await response.json());
          this.message = 'Failed to load quizzes.';
          this.messageClass = 'alert-danger';
        }
      } catch (err) {
        console.error('Network error fetching quizzes:', err);
        this.message = 'Network error loading quizzes.';
        this.messageClass = 'alert-danger';
      }
    },
    async fetchChapters() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters`, { credentials: 'include' });
        if (response.ok) {
          this.chapters = await response.json();
        } else {
          console.error('Error fetching chapters:', await response.json());
        }
      } catch (err) {
        console.error('Network error fetching chapters:', err);
      }
    },
    getChapterName(chapterId) {
      const chapter = this.chapters.find(c => c.id === chapterId);
      return chapter ? chapter.name : 'Unknown Chapter';
    },
    async exportScores() {
      if (!this.selectedQuizId) {
        this.message = 'Please select a quiz to export scores.';
        this.messageClass = 'alert-warning';
        return;
      }

      this.loading = true;
      this.message = '';
      this.messageClass = '';
      this.downloadLink = null;

      try {
        const response = await fetch(`${API_BASE}/api/admin/export-scores`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          // Note: The API call needs to be updated to handle a specific quiz ID if required.
          // The current `routes.py` `export-scores` endpoint exports all scores, so this code is a placeholder for a future, more specific endpoint.
          // For now, it will trigger a full export.
        });

        if (response.ok) {
          const data = await response.json();
          this.message = 'Scores exported successfully! Preparing download...';
          this.messageClass = 'alert-success';
          this.downloadLink = `${API_BASE}${data.filepath}`;
        } else {
          const data = await response.json();
          this.message = `Failed to export scores: ${data.message || response.statusText}`;
          this.messageClass = 'alert-danger';
          console.error('Export error:', data);
        }
      } catch (err) {
        this.message = 'Network error during score export.';
        this.messageClass = 'alert-danger';
        console.error('Network error:', err);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  },
};
</script>
