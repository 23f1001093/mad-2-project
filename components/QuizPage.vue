<template>
  <div class="container mt-5" v-if="quiz">
    <h2>{{ quiz.title }}</h2>
    <p class="text-muted">{{ quiz.description }}</p>

    <div v-if="currentQuestionIndex < quiz.questions.length">
      <div class="card mt-4">
        <div class="card-body">
          <h5 class="card-title">Question {{ currentQuestionIndex + 1 }}</h5>
          <p class="card-text">{{ currentQuestion.text }}</p>
          <div>
            <div
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              class="form-check"
            >
              <input
                class="form-check-input"
                type="radio"
                :id="'option-' + index"
                :value="option"
                v-model="selectedOption"
              />
              <label class="form-check-label" :for="'option-' + index">
                {{ option }}
              </label>
            </div>
          </div>
          <button class="btn btn-primary mt-3" @click="nextQuestion">
            Next
          </button>
        </div>
      </div>
    </div>

    <div v-else class="mt-4">
      <h4>You've completed the quiz!</h4>
      <button class="btn btn-success" @click="submitQuiz">Submit</button>
    </div>
  </div>

  <div v-else class="container mt-5">
    <p>Loading quiz...</p>
  </div>
</template>

<script>
export default {
  name: "QuizPage",
  data() {
    return {
      quiz: null,
      currentQuestionIndex: 0,
      selectedOption: null,
      answers: []
    };
  },
  computed: {
    currentQuestion() {
      return this.quiz.questions[this.currentQuestionIndex];
    }
  },
  methods: {
    async fetchQuiz() {
      const quizId = this.$route.params.id;
      try {
        const res = await fetch(`/api/quiz/${quizId}`);
        this.quiz = await res.json();
      } catch {
        this.quiz = null;
      }
    },
    nextQuestion() {
      if (this.selectedOption === null) return;

      this.answers.push({
        questionId: this.currentQuestion.id,
        answer: this.selectedOption
      });

      this.selectedOption = null;
      this.currentQuestionIndex++;
    },
    async submitQuiz() {
      try {
        const res = await fetch(`/api/quiz/${this.quiz.id}/submit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ answers: this.answers })
        });
        const result = await res.json();
        this.$router.push({ name: 'QuizResult', params: { score: result.score } });
      } catch (error) {
        alert("Error submitting quiz.");
      }
    }
  },
  mounted() {
    this.fetchQuiz();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>