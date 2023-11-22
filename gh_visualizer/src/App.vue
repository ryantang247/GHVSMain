<!-- RepoInfo.vue -->

<template>
  <div class="container">
    <div class="logo-container">
      <!-- Place your logo here -->
      <img src="./assets/company_logo.png" alt="Logo" class="logo" />
    </div>

    <div class="form-container">
      <label>
        Username:
        <input v-model="username" />
      </label>
      <label>
        Repository:
        <input v-model="repo" />
      </label>
      <button @click="postDataToBackend">Fetch Repository Info</button>

      <div v-if="loading">Loading...</div>
      <div v-if="errorMessage != null">Error fetching data</div>
    </div>

    <div class="visualization-container">
      <!-- FileTree Component -->
      <div>
<!--        <FileTree v-for="(element, number) in this.data" :key="number" :treeMap="convertToFileTree(element.file_tree)" />-->
        <FileTree :treeMap="convertToFileTree(this.rawFileTree)" />
      </div>
    </div>

    <GhAPI />
  </div>
</template>
<script>
import FileTree from "@/components/FileTree.vue";
import {Octokit} from "@octokit/rest";
import GhAPI from "@/components/GitAPI.vue";
import data from '@/output.json';
import axios from "axios";
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:5000'
export default {
  components: {GhAPI, FileTree},

  // components: {FileTree},
  data() {
    return {
      // by default, all data types ret
      loaded : false,
      loading: false,
      username: 'TeamNewPipe',
      repo: 'NewPipe',
      rawFileTree: data[0].file_tree,
      filePaths: {},
      currentCommit : {},
      repository: {},
      errorMessage: null,
      overall_tree: {},
      pullJSONData : "",
      pullNumbers: []
    };
  },
  devServer: {
    devServer: {
      proxy: {
        '/send_repo': {
          target: 'http://localhost:5000', // Replace with your Flask server address
          changeOrigin: true,
          ws: true,
        },
      },
    },
  },
  methods: {
    postDataToBackend() {
      const formData = new FormData();
      formData.append('username', this.username); // Replace 'field1' with the actual field name
      formData.append('repo', this.repo);
      const data = new URLSearchParams(formData);

      // Use Axios or another HTTP library to make a request to your Python backend
      axios.post('/send_repo',  data)
          .then(response => {
            // Process the response from the backend
            console.log(response.data);
          })
          .catch(error => {
            // Handle errors
            console.error(error);
          });
    },
    async getFileContents() {
      this.loading = true;
      const octokit = new Octokit({
        auth: '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'
      })

      // const apiUrl = `https://api.github.com/repos/${this.username}/${this.repo}/contents/`;

      try {
        const response = await octokit.request('GET /repos/{owner}/{repo}/pulls/{pull_number}/commits}', {
          owner: this.username,
          repo: this.repo,
          pull_number: this.pull_id,
          branch: 'main',
          headers: {
            'Accept': 'application/vnd.github.v3.raw', // This header indicates that you want the raw content
          },
        });

        // remember to put loaded to true for passing data

        const content = response.data;
        console.log(content)
        this.loading = false;
        this.loaded  =true;

        // Processing data by getting pull requests id and puttting it in array, this is using pull id to get its respective commits
        // this.pullJSONData = response.data
        // this.pullNumbers = this.pullJSONData.map(item => item.number);
        return content;

        } catch{
          this.loading = false;
          this.error = 'Error fetching data!'
        }

      },
    convertToFileTree(fileStructure) {
      const root = { name: "root", children: [] };

      fileStructure.forEach((path) => {
        const parts = path.split('/');
        let currentDir = root;

        parts.forEach((part, index) => {
          const isFile = index === parts.length - 1;
          let node = currentDir.children.find((child) => child.name === part);

          if (!node) {
            // Node doesn't exist, create it
            node = { name: part, value: isFile ? 1 : 0, children: [] };
            currentDir.children.push(node);
          }

          if (isFile) {
            // Increment size for files
            node.value += 1;
          }

          currentDir = node;
        });
      });

      const result = JSON.stringify(root, null, 2)
      // console.log(result)
      return result;
    },
    },
};
</script>

<style scoped>
.clickable-commit {
  cursor: pointer;
  color: blue;
  text-decoration: underline;
  margin-bottom: 5px;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.logo-container {
  margin-bottom: 20px;
}

.logo {
  width: 500px; /* Adjust the width according to your logo size */
  height: auto;
}

label{
  font-family: "Bell MT",serif;
}

.form-container {
  text-align: center;
  margin-bottom: 20px;
}

.visualization-container {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

/* Add more styles as needed */
</style>
