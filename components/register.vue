<template>
  <div class="container mt-5">
    <h2>Register</h2>
    <div v-if="message" :class="['alert mt-3', messageType]">{{ message }}</div>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label class="form-label">Full Name</label> <input v-model="full_name" type="text" class="form-control" required /> </div>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Confirm Password</label>
        <input v-model="confirmPassword" type="password" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="qualification" class="form-label">Qualification</label>
        <input type="text" id="qualification" v-model="qualification" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="dob" class="form-label">Date of Birth</label>
        <input type="date" id="dob" v-model="dob" class="form-control" />
      </div>

      <button class="btn btn-success" type="submit">Register</button>
    </form>
    <p class="mt-3">Already have an account? <router-link to="/login">Login here</router-link></p>
  </div>
</template>

<script>

const API_BASE = 'http://localhost:5001'; 

export default {
  name: "RegisterComponent", 
  data() {
    return {
      full_name: '', 
      email: '',
      password: '',
      confirmPassword: '',
      qualification: '', 
      dob: '',           
      message: '',
      messageType: '' 
    };
  },
  methods: {
    async register() {
     
      this.message = '';
      this.messageType = '';

      if (this.password !== this.confirmPassword) {
        this.message = "Passwords do not match.";
        this.messageType = "alert-danger";
        return;
      }

      try {
        const response = await fetch(`${API_BASE}/api/register`, { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include', 
          body: JSON.stringify({
            full_name: this.full_name, 
            email: this.email,
            password: this.password,
            qualification: this.qualification, 
            dob: this.dob 
          })
        });

        const result = await response.json();

        if (response.ok) { 
          this.message = result.message || 'Registration successful!';
          this.messageType = 'alert-success';
          
          if (this.$router) {
            this.$router.push('/login'); 
          } else {
            console.warn("Vue Router instance not available for redirection.");
          }
        } else {
          
          this.message = result.message || 'Registration failed.';
          this.messageType = 'alert-danger';
        }
      } catch (error) {
        console.error("An error occurred during registration:", error);
        this.message = 'An error occurred during registration.';
        this.messageType = 'alert-danger';
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
</style>