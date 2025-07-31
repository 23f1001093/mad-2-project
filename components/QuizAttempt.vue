<template>
  <div class="container mt-5">
    <h2>Attempt Quiz: {{ quiz.quiz_name }}</h2>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4>Time Left: {{ formattedTimeLeft }}</h4>
      <button class="btn btn-danger" @click="submitQuiz" :disabled="isSubmitting || !quizStarted">Submit Quiz</button>
    </div>

    <div v-if="!quizStarted">
      <p>Click "Start Quiz" when you are ready.</p>
      <button class="btn btn-primary" @click="startQuiz">Start Quiz</button>
    </div>

    <div v-else-if="questions.length > 0">
      <div v-for="(question, index) in questions" :key="question.id" class="card mb-4">
        <div class="card-header">
          Question {{ index + 1 }}: {{ question.question_statement }}
        </div>
        <div class="card-body">
          <div class="form-check" v-for="(option, optIndex) in question.options" :key="optIndex">
            <input
              class="form-check-input"
              type="radio"
              :name="'question_' + question.id"
              :id="'q' + question.id + 'opt' + optIndex"
              :value="option"
              v-model="userAnswers[question.id]"
            />
            <label class="form-check-label" :for="'q' + question.id + 'opt' + optIndex">
              {{ option }}
            </label>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info">
      This quiz has no questions yet.
    </div>

    <div v-if="message" class="alert mt-3" :class="messageType">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { API_BASE } from '../api';

const route = useRoute();
const router = useRouter();
const quizId = route.params.quizId;

const quiz = ref({});
const questions = ref([]);
const userAnswers = ref({}); // { question_id: selected_option_value }
const message = ref('');
const messageType = ref('');
const isSubmitting = ref(false);

const timeLeft = ref(0); // in seconds
const timerInterval = ref(null);
const quizStarted = ref(false);

const formattedTimeLeft = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60);
  const seconds = timeLeft.value % 60;
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
});

const fetchQuizData = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/quizzes/${quizId}/attempt`, { credentials: 'include' });
    if (response.ok) {
      const data = await response.json();
      quiz.value = data;
      questions.value = data.questions;

      // Initialize userAnswers with empty selections
      questions.value.forEach(q => {
        userAnswers.value[q.id] = '';
      });

      // Set time left from quiz duration (e.g., "00:30" -> 30 minutes)
      if (quiz.value.time_duration) {
        const [hours, minutes] = quiz.value.time_duration.split(':').map(Number);
        timeLeft.value = (hours * 3600) + (minutes * 60);
      }
    } else {
      const errorData = await response.json();
      message.value = errorData.message || 'Failed to load quiz.';
      messageType.value = 'alert-danger';
    }
  } catch (error) {
    console.error('Error fetching quiz data:', error);
    message.value = 'An error occurred while loading the quiz.';
    messageType.value = 'alert-danger';
  }
};

const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      clearInterval(timerInterval.value);
      submitQuiz(); // Auto-submit when time runs out
      message.value = 'Time is up! Your quiz has been automatically submitted.';
      messageType.value = 'alert-warning';
    }
  }, 1000);
};

const startQuiz = () => {
  quizStarted.value = true;
  startTimer();
};

const submitQuiz = async () => {
  if (isSubmitting.value) return; // Prevent double submission
  isSubmitting.value = true;
  clearInterval(timerInterval.value); // Stop the timer

  message.value = 'Submitting your quiz...';
  messageType.value = 'alert-info';

  try {
    const response = await fetch(`${API_BASE}/api/quizzes/${quizId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ answers: userAnswers.value }),
    });

    const data = await response.json();
    if (response.ok) {
      message.value = `Quiz submitted successfully! Your score: ${data.score} out of ${data.total_questions}.`;
      messageType.value = 'alert-success';
      // Redirect to user scores page or a results summary
      router.push({ name: 'UserScores' });
    } else {
      message.value = data.message || 'Failed to submit quiz.';
      messageType.value = 'alert-danger';
    }
  } catch (error) {
    console.error('Error submitting quiz:', error);
    message.value = 'An error occurred while submitting the quiz.';
    messageType.value = 'alert-danger';
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchQuizData);

onUnmounted(() => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
  }
});
</script>