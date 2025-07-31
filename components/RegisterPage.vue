<template>
  <div class="container mt-5">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label for="email" class="form-label">Email (Username)</label>
        <input type="email" id="email" v-model="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="fullName" class="form-label">Full Name</label>
        <input type="text" id="fullName" v-model="full_name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="qualification" class="form-label">Qualification</label>
        <input type="text" id="qualification" v-model="qualification" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="dob" class="form-label">Date of Birth</label>
        <input type="date" id="dob" v-model="dob" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <div v-if="message" :class="['alert mt-3', messageType]">{{ message }}</div>
    <p class="mt-3">Already have an account? <router-link to="/login">Login here</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { API_BASE } from '../api';

const router = useRouter();

const email = ref('');
const password = ref('');
const full_name = ref('');
const qualification = ref('');
const dob = ref('');
const message = ref('');
const messageType = ref('');

const register = async () => {
  message.value = '';
  messageType.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/register`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     credentials: 'include', // <--- THIS LINE MUST BE ADDED HERE
     body: JSON.stringify({
       email: email.value,
       password: password.value,
       full_name: full_name.value,
       qualification: qualification.value,
       dob: dob.value,
  }),
});

    const data = await res.json();
    if (res.ok) {
      message.value = data.message;
      messageType.value = 'alert-success';
      // Optionally redirect to login after successful registration
      router.push('/login');
    } else {
      message.value = data.message || 'Registration failed.';
      messageType.value = 'alert-danger';
    }
  } catch (err) {
    console.error(err);
    message.value = 'An error occurred during registration.';
    messageType.value = 'alert-danger';
  }
};
</script>