<template>
  <div>
  <v-card
    class="mx-auto pa-2 overflow-y-auto"
    max-width="400" max-height="400"
  >
      <v-list-subheader>Pull requests</v-list-subheader>

      <v-list-item
        v-for="(pull, i) in pulls"
        :key="i"
        :value="pull"
        color="primary"
        rounded="shaped"
      >
<!--        <template v-slot:prepend>-->
<!--          <v-icon :icon="item.icon"></v-icon>-->
<!--        </template>-->

        <v-list-item-title @click="createTreeMap(pull)" v-text="`${pull.number} ${pull.title}`"></v-list-item-title>
      </v-list-item>
  </v-card>
  </div>
  <div class="treemap-container">
    <div v-if="treeMap1" class="treemap">
      <button class="close-button" @click="removeTreeMap(1)">✕</button>
      <TreeMap :treeMap="convertToFileTree(this.treeMap1.file_tree)" />
    </div>
    <div v-else class="empty-treemap">
      Select TreeMap 1
    </div>
    <div v-if="treeMap2" class="treemap">
      <button class="close-button" @click="removeTreeMap(2)">✕</button>
      <TreeMap :treeMap="convertToFileTree(this.treeMap2.file_tree)" />
    </div>
    <div v-else class="empty-treemap">
      Select TreeMap 2
    </div>
  </div>
</template>
<script>
// import Moveable from "vue3-moveable";
import TreeMap from "@/components/FileTree.vue";

export default {
  name: 'PullList',
  components: {
    TreeMap
    // Moveable,
  },
  props: {
    pulls: {
      type: String,
    },
  },
  data() {
    return {
      data: this.pulls,
      isMouseDown: false,
      treeMap1: null,
      treeMap2:null,
      mouseX: 0,
      mouseY: 0,
    };
  },
  methods:{
    handleMouseDown() {
      this.isMouseDown = true;
    },
    handleMouseUp() {
      this.isMouseDown = false;
    },
    handleMouseMove(event) {
      this.mouseX = event.clientX;
      this.mouseY = event.clientY;
    },
    onDrag({ transform }) {
      this.$refs.target.style.transform = transform;
    },
    onScale({ drag }) {
      this.$refs.target.style.transform = drag.transform;
    },
    onRotate({ drag }) {
      this.$refs.target.style.transform = drag.transform;
    },
    createTreeMap(data){
      if (this.treeMap1 == null) {
        this.treeMap1 = data;
      } else {
        this.treeMap2 = this.treeMap2 == null ? data : this.treeMap2;
      }
    },
    removeTreeMap(index){
      if(index ===1){
        this.treeMap1 = null;
      }else {
        this.treeMap2 = null;

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
  }
  }
}
</script>
<style>
.tracking-area {
  width: 300px;
  height: 200px;
  border: 1px solid #ccc;
  padding: 20px;
  cursor: pointer;
}
.treemap {
  flex: 1; /* Equal width for both treemaps */
  margin-right: 10px; /* Adjust margin between treemaps */
}
.treemap-container {
  display: flex;
  border: 1px solid #ccc; /* Border around the container */
}
.treemap:hover .close-button {
  display: block;
}
.empty-treemap {
  flex: 1; /* Equal width for empty treemaps */
  border: 1px dashed #ccc; /* Border for empty treemaps */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #888;
}
</style>