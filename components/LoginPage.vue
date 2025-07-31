<template>
  <div class="mt-5">
    <h3>Login</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <input v-model="email" class="form-control" placeholder="Email" type="email" required />
      </div>
      <div class="mb-3">
        <input v-model="password" type="password" class="form-control" placeholder="Password" required />
      </div>
      <button class="btn btn-success" type="submit">Login</button>
    </form>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <p class="mt-3">Don't have an account? <router-link to="/register">Register here</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { API_BASE } from '../api'; // Ensure this path is correct relative to LoginPage.vue

const router = useRouter();
const email = ref(''); // Changed to email
const password = ref('');
const error = ref('');

const emit = defineEmits(['set-user']);

const login = async () => {
  error.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/login`, {
      method: 'POST',
      credentials: 'include', // Important for sessions
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value }), // Send email
    });

    if (!res.ok) {
      const err = await res.json();
      error.value = err.message || 'Login failed';
      return;
    }

    const data = await res.json();
    emit('set-user', { id: data.user_id, role: data.role }); // Pass user data up to App.vue
    router.push(data.role === 'admin' ? '/admin-dashboard' : '/user-dashboard'); // Redirect based on role

  } catch (err) {
    console.error(err);
    error.value = 'An error occurred during login.';
  }
};
</script>