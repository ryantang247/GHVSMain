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
      <issueChart></issueChart>
    </div>
    <div>
      <el-table class="overflow-y-auto" :data="pullJSONData.all_pr_data" height="500" style="width: 100%">
        <el-table-column prop="number" label="Pull Number" width="200" />
        <el-table-column prop="created_at" label="Created At" width="400" />
        <el-table-column prop="author" label="Author" width="200" />
        <el-table-column prop="labels_data" label="Labels">
          <template #default="scope">
           <span v-for="(label, index) in scope.row.labels_data" :style="{ backgroundColor: '#' + label.color }" :key="index" class="tag">
            {{ label.name }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <!-- FileTree Component -->
<!--      <div v-if="this.rawFileTree !== ''">-->
<!--&lt;!&ndash;        <FileTree v-for="(element, number) in this.data" :key="number" :treeMap="convertToFileTree(element.file_tree)" />&ndash;&gt;-->
<!--        <FileTree :treeMap="convertToFileTree(this.rawFileTree)" />-->
<!--      </div>-->

      <div v-if="loaded">
        <PullList :pulls="pullJSONData.all_pr_data"></PullList>
      </div>
      <div>

      </div>
    </div>
  </div>
</template>
<script>
// import FileTree from "@/components/FileTree.vue";
// eslint-disable-next-line no-unused-vars
import {Octokit} from "@octokit/rest";
import axios from "axios";
import PullList from "@/components/PullRequestList.vue";
// eslint-disable-next-line no-unused-vars
const config = require('@/auth_config.js');
import picture from '/src/assets/company_logo.png'
import pulls from "./output.json"
import IssueChart from "@/components/Graph.vue";
import {ElTable, ElTableColumn} from "element-plus";

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.2:8080'
export default {
  components: {IssueChart, PullList,ElTable,ElTableColumn},

  data() {
    return {
      // by default, all data types ret
      loaded : true,
      loading: false,
      picture: picture,
      username: 'TeamNewPipe',
      get_closed_merged: false,
      repo: 'NewPipe',
      page_number: 2,
      branch: 'dev',
      pullJSONData : pulls,
      pullJSONDataTable: pulls.all_pr_data
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

      this.loaded = false
      const formData = new FormData();
      formData.append('username', this.username); // Replace 'field1' with the actual field name
      formData.append('repo', this.repo);
      const data = new URLSearchParams(formData);

      // Use Axios or another HTTP library to make a request to your Python backend
      this.loading = true;
      axios.post('/send_repo',  data)
          .then(response => {
            // Process the response from the backend
            this.pullJSONData = response.data
            this.loading = false
            this.loaded  =true;
            console.log(this.pullJSONData);

          })
          .catch(error => {
            this.loaded  =false;
            this.loading = false
            console.error(error);
          });
    },
    async getFileContents() {
      // this.loading = true;
      console.log(this.pullJSONDataTable)
      // const octokit = new Octokit({
      //   auth: config.githubToken
      // })
      //
      // // const apiUrl = `https://api.github.com/repos/${this.username}/${this.repo}/contents/`;
      // // https://api.github.com/search/issues?q=stress+test+label:bug+language:python+state:closed&per_page=100
      // try {
      //
      //   let url = ""
      //
      //   if(this.get_closed_merged){
      //     url = 'repos/{owner}/{repo}/forks'
      //
      //     // url = "GET /repos/{owner}/{repo}/issues?page={page_number}&&state=closed"
      //   }else {
      //     url = 'repos/{owner}/{repo}/forks'
      //     // url = "GET /repos/{owner}/{repo}/issues?page={page_number}&&state=open"
      //   }
      //
      //   const response = await octokit.request(url, {
      //     owner: this.username,
      //     repo: this.repo,
      //     // page_number: this.page_number,
      //     headers: {
      //       'Accept': 'application/vnd.github.v3.raw', // This header indicates that you want the raw content
      //     },
      //   });
      //
      //   // remember to put loaded to true for passing data
      //
      //   const content = response.data;
      //   console.log(content)
      //   this.loading = false;
      //   this.loaded  =true;
      //
      //   // Processing data by getting pull requests id and puttting it in array, this is using pull id to get its respective commits
      //   // this.pullJSONData = response.data
      //   // this.pullNumbers = this.pullJSONData.map(item => item.number);
      //   return content;
      //
      //   } catch{
      //     this.loading = false;
      //     this.error = 'Error fetching data!'
      //   }

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

.table {
  width: 100%;
  margin-bottom: 20px;
  .rows {
    position: absolute;
  }
  .el-table__body-wrapper {
    overflow-y: auto;
  }
  tbody {
    position: relative;
  }
}


label{
  font-family: "Bell MT",serif;
}

.form-container {
  text-align: center;
  margin-bottom: 20px;
}

.tag {
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #0366d6; /* GitHub tag color */
  color: #ffffff; /* Text color */
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
}
/* Add more styles as needed */
</style>
