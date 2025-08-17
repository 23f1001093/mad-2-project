<template>
  <div class="container mt-5 text-center">
    <h2>Quiz Completed!</h2>
    <p class="mt-3">Your score is:</p>
    <h1 class="display-4">{{ score }} / {{ total }}</h1>

    <button class="btn btn-primary mt-4" @click="goToDashboard">
      Go to Dashboard
    </button>
  </div>
</template>

<script>
export default {
  name: "QuizResult",
  data() {
    return {
      score: 0,
      total: 0
    };
  },
  methods: {
    goToDashboard() {
      this.$router.push({ name: "UserDashboard" });
    }
  },
  created() {
    this.score = this.$route.params.score || 0;
    this.total = this.$route.params.total || 10; 
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>