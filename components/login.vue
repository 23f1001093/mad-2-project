<template>
  <div class="container mt-5">
    <h2>Login</h2>
    <div v-if="message" class="alert alert-info">{{ message }}</div>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-primary" type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      email: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        const result = await response.json();

        if (result.success) {
          this.message = 'Login successful!';
          
        } else {
          this.message = result.message || 'Login failed.';
        }
      } catch (error) {
        this.message = 'An error occurred during login.';
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
}
</style>