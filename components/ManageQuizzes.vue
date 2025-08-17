<template>
  <div class="container mt-5">
    <h2>Manage Quizzes</h2>
    <router-link to="/create-quiz" class="btn btn-success mb-3">Create New Quiz</router-link>

    <div v-if="quizzes.length === 0" class="alert alert-info">
      No quizzes found.
    </div>
    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th>Quiz Name</th>
          <th>Subject</th>
          <th>Chapter</th>
          <th>Duration</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes" :key="quiz.id">
          <td>{{ quiz.name }}</td>
          <td>{{ getSubjectName(getChapterSubjectId(quiz.chapter_id)) }}</td>
          <td>{{ getChapterName(quiz.chapter_id) }}</td>
          <td>{{ quiz.time_duration }}</td>
          <td>
            <router-link :to="{ name: 'ManageQuestions', params: { quizId: quiz.id } }" class="btn btn-sm btn-info me-2">
              Manage Questions
            </router-link>
            <router-link :to="{ name: 'ViewResults', params: { quizId: quiz.id } }" class="btn btn-sm btn-primary me-2">
              View Results
            </router-link>
            <button class="btn btn-sm btn-warning me-2" @click="editQuiz(quiz)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteQuiz(quiz.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="editingQuiz" class="mt-4 p-3 border rounded bg-light">
        <h4>Edit Quiz: {{ editingQuiz.name }}</h4>
        <form @submit.prevent="saveQuizEdit">
            <div class="mb-3">
                <label for="editQuizName" class="form-label">Quiz Name</label>
                <input type="text" id="editQuizName" v-model="editingQuiz.name" class="form-control" required />
            </div>
            <div class="mb-3">
                <label for="editQuizDuration" class="form-label">Duration (HH:MM)</label>
                <input type="text" id="editQuizDuration" v-model="editingQuiz.time_duration" class="form-control" placeholder="HH:MM" required />
            </div>
            <div class="mb-3">
                <label for="editQuizRemarks" class="form-label">Remarks</label>
                <textarea id="editQuizRemarks" v-model="editingQuiz.remarks" class="form-control"></textarea>
            </div>
            <div class="mb-3">
                <label for="editQuizChapter" class="form-label">Chapter</label>
                <select id="editQuizChapter" v-model="editingQuiz.chapter_id" class="form-select" required>
                    <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                        {{ chapter.name }} ({{ getSubjectName(chapter.subject_id) }})
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

import { API_BASE } from '../api';

export default {
  name: "ManageQuizzes",
  data() {
    return {
      quizzes: [],
      editingQuiz: null,
      chapters: [],
      subjects: [],
      message: '', // For general messages
      messageClass: '', // For styling messages
    };
  },
  methods: {
    async fetchQuizzes() {
      this.message = ''; 
      this.messageClass = '';
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes`, { credentials: 'include' });
        const data = await response.json();
        if (response.ok) {
          this.quizzes = data.quizzes || [];
        } else {
          this.message = data.message || `Error fetching quizzes: ${response.statusText}`;
          this.messageClass = 'alert-danger';
          console.error('Error fetching quizzes:', data.message);
        }
      } catch (err) {
        this.message = 'Network error fetching quizzes.';
        this.messageClass = 'alert-danger';
        console.error('Network error fetching quizzes:', err);
      }
    },
    async fetchChaptersAndSubjects() {
        try {
            const [chaptersRes, subjectsRes] = await Promise.all([
                
                fetch(`${API_BASE}/api/admin/chapters`, { credentials: 'include' }),
                
                fetch(`${API_BASE}/api/admin/subjects`, { credentials: 'include' })
            ]);

            if (!chaptersRes.ok || !subjectsRes.ok) {
                const chaptersError = chaptersRes.ok ? null : await chaptersRes.json().catch(() => ({}));
                const subjectsError = subjectsRes.ok ? null : await subjectsRes.json().catch(() => ({}));
                this.message = `Error loading dependencies: ${chaptersError?.message || subjectsError?.message || 'Server error'}`;
                this.messageClass = 'alert-danger';
                console.error('Error loading chapters:', chaptersError);
                console.error('Error loading subjects:', subjectsError);
                return;
            }

            this.chapters = await chaptersRes.json();
            this.subjects = await subjectsRes.json();
        } catch (error) {
            this.message = 'Network error fetching chapters or subjects.';
            this.messageClass = 'alert-danger';
            console.error('Network error fetching chapters or subjects:', error);
        }
    },
    getSubjectName(subjectId) {
      const subject = this.subjects.find(s => s.id === subjectId);
      return subject ? subject.name : 'Unknown Subject';
    },
    getChapterName(chapterId) {
        const chapter = this.chapters.find(c => c.id === chapterId);
        return chapter ? chapter.name : 'Unknown Chapter';
    },
    getChapterSubjectId(chapterId) {
        const chapter = this.chapters.find(c => c.id === chapterId);
        return chapter ? chapter.subject_id : null;
    },
    editQuiz(quiz) {
      this.editingQuiz = { ...quiz };
    },
    async saveQuizEdit() {
        if (!this.editingQuiz) return;
        this.message = '';
        this.messageClass = '';
        try {
            
            const response = await fetch(`${API_BASE}/api/admin/quizzes/${this.editingQuiz.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(this.editingQuiz)
            });
            if (response.ok) {
                this.message = 'Quiz updated successfully!';
                this.messageClass = 'alert-success';
                this.editingQuiz = null; 
                this.fetchQuizzes(); 
            } else {
                const data = await response.json();
                this.message = `Failed to update quiz: ${data.message || response.statusText}`;
                this.messageClass = 'alert-danger';
                console.error('Error updating quiz:', data.message);
            }
        } catch (error) {
            this.message = 'Network error updating quiz.';
            this.messageClass = 'alert-danger';
            console.error('Network error updating quiz:', error);
        }
    },
    cancelEdit() {
        this.editingQuiz = null;
        this.message = ''; 
        this.messageClass = '';
    },
    async deleteQuiz(quizId) {
      if (!confirm('Are you sure you want to delete this quiz? This will also delete its questions and scores.')) return;
      this.message = '';
      this.messageClass = '';

      try {
       
        const response = await fetch(`${API_BASE}/api/admin/quizzes/${quizId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        const data = await response.json();
        if (response.ok) {
          this.message = data.message;
          this.messageClass = 'alert-success';
          this.quizzes = this.quizzes.filter(q => q.id !== quizId); 
        } else {
          this.message = `Failed to delete quiz: ${data.message || response.statusText}`;
          this.messageClass = 'alert-danger';
          console.error('Error deleting quiz:', data.message);
        }
      } catch (err) {
        this.message = 'Network error deleting quiz.';
        this.messageClass = 'alert-danger';
        console.error('Network error deleting quiz:', err);
      }
    },
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChaptersAndSubjects();
  },
};
</script>