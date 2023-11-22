<template>
  <div>
    <h1>GitHub Repositories</h1>

    <form @submit.prevent="getRepositories">
      <label for="username">GitHub Username:</label>
      <input v-model="username" type="text" id="username" name="username" required>
      <button type="submit">Get Repositories</button>
    </form>

    <div v-if="repositories.length > 0">
      <h2>Public Repositories:</h2>
      <ul>
        <li v-for="repo in repositories" :key="repo.id">{{ repo.name }}</li>
      </ul>
    </div>

    <div v-else>
      <p>No public repositories found.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      username: '',
      repositories: [],
    };
  },
  methods: {
    async getRepositories() {
      try {
        const response = await fetch(`https://api.github.com/users/${this.username}/repos`);
        this.repositories = await response.json();
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    },
  },
};
</script>
