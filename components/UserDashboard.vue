<template>
  <div class="container mt-5">
    <h2>Welcome, {{ user?.full_name || 'User' }}</h2>
    <h4>Available Quizzes</h4>

    <div v-if="quizzes.length === 0" class="alert alert-info">
      No quizzes available at the moment. Check back later!
    </div>
    <ul class="list-group" v-else>
      <li class="list-group-item d-flex justify-content-between align-items-center" v-for="quiz in quizzes" :key="quiz.id">
        <div>
          <h5>{{ quiz.name }}</h5>
          <p class="mb-1">Subject: {{ quiz.subject_name }} | Chapter: {{ quiz.chapter_name }}</p>
          <p class="mb-1">Duration: {{ quiz.time_duration }}</p>
          <p class="text-muted">{{ quiz.remarks }}</p>
        </div>
        <router-link :to="{ name: 'QuizAttempt', params: { quizId: quiz.id } }" class="btn btn-primary">
          Start Quiz
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE } from '../api';

const props = defineProps(['user']); 
const quizzes = ref([]);

const fetchQuizzes = async () => {
  try {
    
    const response = await fetch(`${API_BASE}/api/quizzes`, { credentials: 'include' });
    
    if (response.ok) {
      const data = await response.json();
      quizzes.value = data.quizzes;
    } else {
      console.error('Failed to fetch quizzes for user.');
    }
  } catch (error) {
    console.error('Error fetching quizzes:', error);
  }
};

onMounted(fetchQuizzes);
</script>
