<template>
  <div>
    <h1>{{ msg }}</h1>
    <table>
      <thead>
      <tr>
        <th>Author</th>
        <th>Date</th>
        <th>Message</th>
      </tr>
      </thead>
      <tbody>
<!--      <tr v-for="(author) in commitsByAuthor" :key="author">-->
<!--        <td colspan="3">-->
<!--          <h2>{{ author }}</h2>-->
<!--        </td>-->
<!--      </tr>-->
      <tr v-for="commit in flattenedCommits" :key="commit.sha">
        <td>{{ commit.commit.author.name }}</td>
        <td>{{ commit.commit.author.date }}</td>
        <td>{{ commit.commit.message }}</td>
      </tr>
      </tbody>
    </table>
<!--    <div>-->
<!--    <FileTree :fileTree="fileTree" />-->
<!--    </div>-->
  </div>
</template>

<script>
import { Octokit } from '@octokit/rest';
// eslint-disable-next-line no-unused-vars
import axios from "axios";
// import FileTree from "@/components/FileTree.vue";

export default {
  name: 'GhAPI',
  // components: {FileTree},
  props: {
    msg: String
  },
  // owner: 'ryantang247',
  // repo: 'DL-project',
  data() {
    return {
      commitsByAuthor: {},
      fileTree: {}
    };
  },
  async created() {
    // Your personal access token
    const accessToken = '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';
    // eslint-disable-next-line no-unused-vars
    const apiUrl = `https://api.github.com/repos/${this.owner}/${this.repo}/contents/`;
    const octokit = new Octokit({
      auth: accessToken,
    });

    try {
      // Get commits
      const commitsResponse = await octokit.repos.listCommits({
        owner: 'ryantang247',
        repo: 'DL-project',
      });

      await this.fetchAndBuildFileTree();
      this.commitsByAuthor = this.organizeCommitsByAuthor(commitsResponse.data);

      console.log('Commits by Author:', this.commitsByAuthor);
    } catch (error) {
      console.error('Error:', error.message);
    }
  },
  computed: {
    flattenedCommits() {
      // Flatten the commitsByAuthor object into a single array
      return Object.values(this.commitsByAuthor).reduce((acc, commits) => acc.concat(commits), []);
    }
  },
  methods: {
    async fetchAndBuildFileTree() {
      // Your personal access token
      const apiUrl = `https://api.github.com/repos/${this.owner}/${this.repo}/contents/`;

      try {
        // Get file tree
        const response = await axios.get(apiUrl);
        this.fileTree = this.buildFileTree(response.data);
      } catch (error) {
        console.error('Error fetching files:', error);
      }
    },

    buildFileTree(files) {
      const fileTree = {};

      files.forEach(file => {
        const pathComponents = file.path.split('/');
        let currentNode = fileTree;

        pathComponents.forEach(component => {
          currentNode[component] = currentNode[component] || {};
          currentNode = currentNode[component];
        });
      });

      return fileTree;
    },
    organizeCommitsByAuthor(commits) {
      const commitsByAuthor = {};

      commits.forEach(commit => {
        const authorName = commit.commit.author.name;

        // Create an array for the author if it doesn't exist
        if (!commitsByAuthor[authorName]) {
          commitsByAuthor[authorName] = [];
        }

        // Add the commit to the author's array
        commitsByAuthor[authorName].push(commit);
      });

      return commitsByAuthor;
    }


  }
};
</script>
