<template>
  <div class="container mt-5">
    <h2>Manage Questions for Quiz: {{ quiz.name }}</h2>
    <div v-if="!quizId || loading" class="alert alert-info">
      Loading quiz details...
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else>
      <div class="card p-4 mb-4">
        <h4>Add New Question</h4>
        <form @submit.prevent="addQuestion">
          <div class="mb-3">
            <label for="questionStatement" class="form-label">Question Statement</label>
            <textarea id="questionStatement" v-model="newQuestion.question_statement" class="form-control" required></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="option1" class="form-label">Option 1</label>
              <input type="text" id="option1" v-model="newQuestion.options[0]" class="form-control" required />
            </div>
            <div class="col-md-6 mb-3">
              <label for="option2" class="form-label">Option 2</label>
              <input type="text" id="option2" v-model="newQuestion.options[1]" class="form-control" required />
            </div>
            <div class="col-md-6 mb-3">
              <label for="option3" class="form-label">Option 3</label>
              <input type="text" id="option3" v-model="newQuestion.options[2]" class="form-control" required />
            </div>
            <div class="col-md-6 mb-3">
              <label for="option4" class="form-label">Option 4</label>
              <input type="text" id="option4" v-model="newQuestion.options[3]" class="form-control" required />
            </div>
          </div>
          <div class="mb-3">
            <label for="correctOption" class="form-label">Correct Option</label>
            <select id="correctOption" v-model="newQuestion.correct_option" class="form-select" required>
              <option disabled value="">Select Correct Option</option>
              <option v-for="(option, index) in newQuestion.options" :key="index" :value="option">{{ option }}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Add Question</button>
        </form>
      </div>

      <h4>Existing Questions</h4>
      <div v-if="questions.length === 0" class="alert alert-warning">
        No questions added to this quiz yet.
      </div>
      <div v-else>
        <div v-for="question in questions" :key="question.id" class="card p-3 mb-3">
          <h5>{{ question.question_statement }}</h5>
          <ul>
            <li>Option 1: {{ question.option1 }} <span v-if="question.option1 === question.correct_option" class="text-success">(Correct)</span></li>
            <li>Option 2: {{ question.option2 }} <span v-if="question.option2 === question.correct_option" class="text-success">(Correct)</span></li>
            <li>Option 3: {{ question.option3 }} <span v-if="question.option3 === question.correct_option" class="text-success">(Correct)</span></li>
            <li>Option 4: {{ question.option4 }} <span v-if="question.option4 === question.correct_option" class="text-success">(Correct)</span></li>
          </ul>
          <div class="d-flex justify-content-end">
            <button class="btn btn-sm btn-danger" @click="deleteQuestion(question.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="message" class="alert mt-3" :class="messageClass">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { API_BASE } from '../api';

export default {
  name: "ManageQuestions",
  data() {
    return {
      quizId: null,
      quiz: {},
      questions: [],
      newQuestion: {
        question_statement: '',
        options: ['', '', '', ''],
        correct_option: ''
      },
      loading: true,
      error: null,
      message: '',
      messageClass: '',
    };
  },
  watch: {
    
    '$route.params.quizId': {
      immediate: true, 
      handler(newQuizId) {
        if (newQuizId) {
          this.quizId = newQuizId;
          this.fetchQuizDetails();
          this.fetchQuestions();
        } else {
          // Handle case where quizId is not in the URL
          this.error = 'Quiz ID not found in URL.';
          this.loading = false;
        }
      }
    }
  },
  methods: {
    async fetchQuizDetails() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes/${this.quizId}`, { credentials: 'include' });
        if (response.ok) {
          this.quiz = await response.json();
        } else {
          this.error = `Failed to fetch quiz details: ${await response.text()}`;
          console.error(this.error);
        }
      } catch (err) {
        this.error = 'Network error fetching quiz details.';
        console.error(this.error, err);
      } finally {
        this.loading = false;
      }
    },
    async fetchQuestions() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes/${this.quizId}/questions`, { credentials: 'include' });
        if (response.ok) {
          this.questions = await response.json();
        } else {
          this.error = `Failed to fetch questions: ${await response.text()}`;
          console.error(this.error);
        }
      } catch (err) {
        this.error = 'Network error fetching questions.';
        console.error(this.error, err);
      } finally {
        this.loading = false;
      }
    },
    async addQuestion() {
      if (!this.quizId) {
        this.message = 'Error: Quiz ID is missing.';
        this.messageClass = 'alert-danger';
        return;
      }

      this.message = '';
      this.messageClass = '';

      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes/${this.quizId}/questions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.newQuestion)
        });

        const data = await response.json();
        if (response.ok) {
          this.message = 'Question added successfully!';
          this.messageClass = 'alert-success';
          // Reset form and refresh questions
          this.newQuestion = {
            question_statement: '',
            options: ['', '', '', ''],
            correct_option: ''
          };
          this.fetchQuestions();
        } else {
          this.message = `Error adding question: ${data.message || response.statusText}`;
          this.messageClass = 'alert-danger';
          console.error('Error adding question:', data);
        }
      } catch (err) {
        this.message = 'Network error adding question.';
        this.messageClass = 'alert-danger';
        console.error('Network error adding question:', err);
      }
    },
    async deleteQuestion(questionId) {
        if (!confirm('Are you sure you want to delete this question?')) return;
        this.message = '';
        this.messageClass = '';

        try {
            const response = await fetch(`${API_BASE}/api/admin/questions/${questionId}`, {
                method: 'DELETE',
                credentials: 'include'
            });

            const data = await response.json();
            if (response.ok) {
                this.message = data.message;
                this.messageClass = 'alert-success';
                this.questions = this.questions.filter(q => q.id !== questionId);
            } else {
                this.message = `Failed to delete question: ${data.message || response.statusText}`;
                this.messageClass = 'alert-danger';
                console.error('Error deleting question:', data);
            }
        } catch (err) {
            this.message = 'Network error deleting question.';
            this.messageClass = 'alert-danger';
            console.error('Network error deleting question:', err);
        }
    }
  },
};
</script>
