<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">QuizMaster</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item" v-if="isAuthenticated && userRole === 'user'">
            <router-link to="/user-dashboard" class="nav-link">User Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="isAuthenticated && userRole === 'user'">
            <router-link to="/user-scores" class="nav-link">My Scores</router-link>
          </li>
          <li class="nav-item dropdown" v-if="isAuthenticated && userRole === 'admin'">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Admin
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><router-link to="/admin-dashboard" class="dropdown-item">Admin Dashboard</router-link></li>
              <li><router-link to="/manage-subjects" class="dropdown-item">Manage Subjects</router-link></li>
              <li><router-link to="/manage-chapters" class="dropdown-item">Manage Chapters</router-link></li>
              <li><router-link to="/manage-quizzes" class="dropdown-item">Manage Quizzes</router-link></li>
              <li><router-link to="/export-scores" class="dropdown-item">Export Scores</router-link></li>
              </ul>
          </li>
        </ul>
        <div class="d-flex">
          <button class="btn btn-outline-primary me-2" @click="goTo('/login')" v-if="!isAuthenticated">Login</button>
          <button class="btn btn-outline-success me-2" @click="goTo('/register')" v-if="!isAuthenticated">Register</button>
          <button class="btn btn-outline-danger" @click="logout" v-if="isAuthenticated">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  isAuthenticated: Boolean,
  userRole: String,
});

const emit = defineEmits(['logout']);

const goTo = (path) => {
  router.push(path);
};

const logout = () => {
  emit('logout');
};
</script>

<style scoped>
.navbar {
  border-bottom: 1px solid #ccc;
}
</style>