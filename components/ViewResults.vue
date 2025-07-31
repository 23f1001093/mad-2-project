<template>
  <div class="container mt-5">
    <h2>Results for Quiz: {{ quizName }}</h2>

    <router-link to="/admin-dashboard" class="btn btn-secondary mb-3">
      Back to Admin Dashboard
    </router-link>

    <div v-if="results.length === 0" class="alert alert-info">
      No one has attempted this quiz yet.
    </div>
    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th>User Name</th>
          <th>User Email</th>
          <th>Score</th>
          <th>Attempt Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(result, index) in results" :key="index">
          <td>{{ result.user_name }}</td>
          <td>{{ result.user_email }}</td>
          <td>{{ result.scored }} / {{ result.total_possible }}</td>
          <td>{{ result.attempt_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { API_BASE } from '../api';

const route = useRoute();
const quizId = route.params.quizId;

const quizName = ref('');
const results = ref([]);

const fetchResults = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/admin/quizzes/${quizId}/results`, { credentials: 'include' });
    if (response.ok) {
      const data = await response.json();
      quizName.value = data.quiz_name;
      results.value = data.results;
    } else {
      console.error('Failed to fetch quiz results.');
    }
  } catch (error) {
    console.error('Error fetching results:', error);
  }
};

onMounted(fetchResults);
</script>