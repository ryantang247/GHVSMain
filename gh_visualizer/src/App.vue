<!-- RepoInfo.vue -->

<template>
  <div class="container">
    <div class="logo-container">
      <!-- Place your logo here -->
      <img :src="this.picture" alt="Logo"/>
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
      <label>
        Repository:
        <input v-model="branch" />
      </label>
      <button @click="postDataToBackend">Fetch Repository Info</button>
      <button @click="getFileContents">Test Get Modified File</button>
      <div v-if="loading">Loading...</div>
      <div v-if="errorMessage != null">Error fetching data</div>
    </div>

    <div>
      <!-- FileTree Component -->
<!--      <div v-if="this.rawFileTree !== ''">-->
<!--&lt;!&ndash;        <FileTree v-for="(element, number) in this.data" :key="number" :treeMap="convertToFileTree(element.file_tree)" />&ndash;&gt;-->
<!--        <FileTree :treeMap="convertToFileTree(this.rawFileTree)" />-->
<!--      </div>-->
      <div v-if="this.pullJSONData">
        <PullList :pulls="pullJSONData"></PullList>
      </div>
      <div>

      </div>
    </div>
  </div>
</template>
<script>
// import FileTree from "@/components/FileTree.vue";
import {Octokit} from "@octokit/rest";
import axios from "axios";
import PullList from "@/components/PullRequestList.vue";
const config = require('@/auth_config.js');
import picture from '/src/assets/company_logo.png'
import pulls from "./output.json"

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.2:8080'
export default {
  components: {PullList},

  // components: {FileTree},
  data() {
    return {
      // by default, all data types ret
      loaded : false,
      loading: false,
      picture: picture,
      username: 'TeamNewPipe',
      repo: 'NewPipe',
      branch: 'dev',
      rawFileTree: "",
      repository: {},
      overall_tree: {},
      pullJSONData : pulls,
    };
  },
  devServer: {
    devServer: {
      proxy: {
        '/send_repo': {
          target: 'http://127.0.0.2:8080', // Replace with your Flask server address
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
            this.pullJSONData = response.data
            this.rawFileTree = this.pullJSONData[0].file_tree
            console.log(this.rawFileTree)
            console.log(this.pullJSONData);

          })
          .catch(error => {
            // Handle errors
            console.error(error);
          });
    },
    async getFileContents() {
      this.loading = true;
      const octokit = new Octokit({
        auth: config.githubToken
      })

      // const apiUrl = `https://api.github.com/repos/${this.username}/${this.repo}/contents/`;

      try {
        const response = await octokit.request('GET /repos/{owner}/{repo}/pulls', {
          owner: this.username,
          repo: this.repo,
          branch: this.branch,
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

/* Add more styles as needed */
</style>
