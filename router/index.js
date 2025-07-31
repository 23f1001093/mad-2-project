// index.js
import { createRouter, createWebHistory } from 'vue-router';

// Admin Components
import AdminDashboard from '../components/AdminDashboard.vue';
import ManageSubjects from '../components/ManageSubjects.vue';
import ManageChapters from '../components/ManageChapters.vue';
import CreateQuiz from '../components/create_quiz.vue';
import ManageQuizzes from '../components/ManageQuizzes.vue';
import ManageQuestions from '../components/ManageQuestions.vue';
import ViewResults from '../components/ViewResults.vue';
import ExportScores from '../components/ExportScores.vue';

// User & Auth Components
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import UserDashboard from '../components/UserDashboard.vue';
import QuizAttempt from '../components/QuizAttempt.vue';
import UserScores from '../components/UserScores.vue';

const routes = [
  { path: '/', redirect: '/login' }, // Redirect root to login
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },

  // Admin Routes
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    path: '/manage-subjects',
    name: 'ManageSubjects',
    component: ManageSubjects,
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    path: '/manage-chapters',
    name: 'ManageChapters',
    component: ManageChapters,
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    path: '/create-quiz',
    name: 'CreateQuiz',
    component: CreateQuiz,
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    path: '/manage-quizzes',
    name: 'ManageQuizzes',
    component: ManageQuizzes,
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    // This is the correct way to define a route with a dynamic parameter.
    // The component can now access `this.$route.params.quizId`.
    path: '/manage-questions/:quizId',
    name: 'ManageQuestions',
    component: ManageQuestions,
    props: true, // This allows the quizId to be passed directly as a prop to the component
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    path: '/admin/quizzes/:quizId/results',
    name: 'ViewResults',
    component: ViewResults,
    props: true,
    meta: { requiresAuth: true, adminOnly: true },
  },
  {
    path: '/export-scores',
    name: 'ExportScores',
    component: ExportScores,
    meta: { requiresAuth: true, adminOnly: true },
  },

  // User Routes
  {
    path: '/user-dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/quiz/:quizId/attempt',
    name: 'QuizAttempt',
    component: QuizAttempt,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/user-scores',
    name: 'UserScores',
    component: UserScores,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigation guard
router.beforeEach(async (to, from, next) => {
  let userData = null;
  try {
    const res = await fetch('http://localhost:5001/api/me', { credentials: 'include' });

    if (res.ok) {
      userData = await res.json();
    } else {
      userData = null;
    }
  } catch (err) {
    console.error("Error fetching user data:", err);
    userData = null;
  }

  // If route requires auth and user is not logged in, redirect to login
  if (to.meta.requiresAuth && !userData) {
    if (to.path !== '/login') {
      return next('/login');
    } else {
      return next();
    }
  }

  // If route requires admin and user is not admin, redirect
  if (to.meta.adminOnly && (!userData || userData.role !== 'admin')) {
    return next('/user-dashboard');
  }

  // If user is already authenticated and trying to go to login/root, redirect to their dashboard
  if ((to.path === '/login' || to.path === '/') && userData) {
    return next(userData.role === 'admin' ? '/admin-dashboard' : '/user-dashboard');
  }

  next();
});

export default router;
