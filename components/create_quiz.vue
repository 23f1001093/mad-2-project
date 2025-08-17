<template>
  <div class="container mt-5">
    <h2>Create New Quiz</h2>
    <form @submit.prevent="createQuiz">
      <div class="mb-3">
        <label for="quizName" class="form-label">Quiz Name</label>
        <input type="text" class="form-control" id="quizName" v-model="quizName" required>
      </div>
      <div class="mb-3">
        <label for="subjectSelect" class="form-label">Subject</label>
        <select class="form-select" id="subjectSelect" v-model="selectedSubjectId" @change="fetchChapters" required>
          <option value="" disabled>Select Subject</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">{{ subject.name }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="chapterSelect" class="form-label">Chapter</label>
        <select class="form-select" id="chapterSelect" v-model="selectedChapterId" :disabled="!chapters.length" required>
          <option value="" disabled>Select Chapter</option>
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="duration" class="form-label">Duration (HH:MM)</label>
        <input type="text" class="form-control" id="duration" v-model="duration" pattern="\d{2}:\d{2}" placeholder="e.g., 00:30 for 30 mins" required>
      </div>
      <div class="mb-3">
        <label for="remarks" class="form-label">Remarks (Optional)</label>
        <textarea class="form-control" id="remarks" rows="3" v-model="remarks"></textarea>
      </div>
      <div v-if="message" :class="['alert', messageClass]">{{ message }}</div>
      <button type="submit" class="btn btn-primary mt-3">Create Quiz</button>
    </form>
  </div>
</template>

<script>
import { API_BASE } from '../api';

export default {
  name: "CreateQuiz",
  data() {
    return {
      quizName: '',
      subjects: [],
      selectedSubjectId: '',
      chapters: [],
      selectedChapterId: '',
      duration: '',
      remarks: '',
      message: '',
      messageClass: '',
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/subjects`, {
          credentials: 'include'
        });
        if (response.ok) {
          this.subjects = await response.json();
        } else {
          this.message = 'Failed to fetch subjects.';
          this.messageClass = 'alert-danger';
          console.error('Failed to fetch subjects.');
        }
      } catch (error) {
        this.message = 'Network error: Could not connect to the API.';
        this.messageClass = 'alert-danger';
        console.error('Network error fetching subjects:', error);
      }
    },
    async fetchChapters() {
      if (!this.selectedSubjectId) {
        this.chapters = [];
        this.selectedChapterId = '';
        return;
      }
      try {
        const response = await fetch(`${API_BASE}/api/admin/subjects/${this.selectedSubjectId}/chapters`, {
          credentials: 'include'
        });
        if (response.ok) {
          this.chapters = await response.json();
          this.selectedChapterId = ''; 
        } else {
          this.message = 'Failed to fetch chapters.';
          this.messageClass = 'alert-danger';
          console.error('Failed to fetch chapters:', response.statusText);
        }
      } catch (error) {
        this.message = 'Network error: Could not connect to the API.';
        this.messageClass = 'alert-danger';
        console.error('Network error fetching chapters:', error);
      }
    },
    async createQuiz() {
      this.message = '';
      this.messageClass = '';
      const quizData = {
        name: this.quizName,
        chapter_id: this.selectedChapterId,
        time_duration: this.duration,
        remarks: this.remarks
      };
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify(quizData),
        });

        const data = await response.json();
        if (response.ok) {
          this.message = 'Quiz created successfully!';
          this.messageClass = 'alert-success';
          
        } else {
          this.message = data.message || 'Failed to create quiz.';
          this.messageClass = 'alert-danger';
          console.error('Failed to create quiz:', data.message);
        }
      } catch (error) {
        this.message = 'Network error: Could not connect to the API.';
        this.messageClass = 'alert-danger';
        console.error('Network error creating quiz:', error);
      }
    }
  },
  mounted() {
    this.fetchSubjects();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
