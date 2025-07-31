<template>
  <div class="container mt-5">
    <h2>My Quiz Scores</h2>

    <div v-if="scores.length === 0" class="alert alert-info">
      You haven't attempted any quizzes yet.
    </div>
    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th>Quiz Name</th>
          <th>Score</th>
          <th>Attempt Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="score in scores" :key="score.score_id">
          <td>{{ score.quiz_name }}</td>
          <td>{{ score.scored }} / {{ score.total_possible }}</td>
          <td>{{ score.attempt_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE } from '../api';

const scores = ref([]);

const fetchScores = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/user/scores`, { credentials: 'include' });
    if (response.ok) {
      scores.value = await response.json();
    } else {
      console.error('Failed to fetch user scores.');
    }
  } catch (error) {
    console.error('Error fetching scores:', error);
  }
};

onMounted(fetchScores);
</script>