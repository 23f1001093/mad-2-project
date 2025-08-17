// App.vue (Ensure redirects based on role from fetchUser)
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NavBar from './components/NavBar.vue'; 

const router = useRouter();
const user = ref(null);
const isAuthenticated = ref(false);

const fetchUser = async () => {
  try {
    const res = await fetch('http://localhost:5001/api/me', { credentials: 'include' });
    if (res.ok) {
      const userData = await res.json();
      user.value = userData;
      isAuthenticated.value = true;
      
      if (router.currentRoute.value.path === '/login' || router.currentRoute.value.path === '/') {
        router.push(user.value.role === 'admin' ? '/admin-dashboard' : '/user-dashboard');
      }
    } else {
      user.value = null;
      isAuthenticated.value = false;
      
      if (router.currentRoute.value.meta.requiresAuth && router.currentRoute.value.path !== '/login') {
        router.push('/login');
      }
    }
  } catch (err) {
    console.error(err);
    isAuthenticated.value = false;
    if (router.currentRoute.value.meta.requiresAuth && router.currentRoute.value.path !== '/login') {
      router.push('/login');
    }
  }
};

const logout = async () => {
  await fetch('http://localhost:5001/api/logout', {
    method: 'POST',
    credentials: 'include',
  });
  user.value = null;
  isAuthenticated.value = false;
  router.push('/login');
};

const setUser = (userData) => {
  user.value = userData;
  isAuthenticated.value = !!userData;
};

onMounted(fetchUser);
</script>

<template>
  <div>
    <NavBar :isAuthenticated="isAuthenticated" :userRole="user?.role" @logout="logout" />
    <div class="container mt-4">
      <router-view :user="user" @set-user="setUser" />
    </div>
  </div>
</template>