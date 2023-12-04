<template>
  <div class="flex-container">
  <div>
  <v-card
    class="mx-auto pa-2 overflow-y-auto overflow-x:auto"
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
        <div class="tooltip">
        <v-list-item-title  @click="createTreeMap(pull)"  v-text="`${pull.number} ${pull.title}`">
        </v-list-item-title>
          <span class="tooltiptext">
            <v-row v-for="(label, index) in pull.labels_data" :key="index" align="center">
            <v-col :style="{ backgroundColor: '#' + label.color, color: getContrastColor(label.color)
            }" class="label">
              {{ label.name }}
            </v-col>
          </v-row>
          </span>
        </div>
      </v-list-item>
  </v-card>
  </div>
  <div class="treemap-container">
    <div v-if="treeMap1" class="treemap">
      <button class="close-button" @click="removeTreeMap(1)">✕</button>
      <TreeMap :treeMap="convertToFileTree(this.treeMap1.modified_files_data)" />
    </div>
    <div v-else class="empty-treemap">
      Select TreeMap 1
    </div>
    <div v-if="treeMap2" class="treemap">
      <button class="close-button" @click="removeTreeMap(2)">✕</button>
      <TreeMap :treeMap="convertToFileTree(this.treeMap2.modified_files_data)" />
    </div>
    <div v-else class="empty-treemap">
      Select TreeMap 2
    </div>
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
      tooltipIndex: null,
      treeMap1: null,
      treeMap2:null,
      mouseX: 0,
      mouseY: 0,
    };
  },
  methods:{
    updateTooltipPosition(event) {
      if (this.tooltipIndex !== null) {
        const tooltip = this.$refs.tooltip;
        if (tooltip) {
          const x = event ? event.clientX : 0;
          const y = event ? event.clientY : 0;

          this.tooltipStyle = {
            display: 'block',
            left: `${x + 10}px`, // Adjust the offset as needed
            top: `${y + 10}px`, // Adjust the offset as needed
          };
        }
      }
      },
    showTooltip(index) {
      this.tooltipIndex = index;
      this.updateTooltipPosition();
    },
    hideTooltip() {
      this.tooltipIndex = null;
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
    getContrastColor(hexColor) {
      const r = parseInt(hexColor.substring(0, 2), 16);
      const g = parseInt(hexColor.substring(2, 4), 16);
      const b = parseInt(hexColor.substring(4, 6), 16);

      // Calculate luminance
      const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

      // Return 'white' for dark backgrounds, 'black' for light backgrounds
      return luminance > 0.5 ? 'black' : 'white';
    },
    convertToFileTree(fileStructure) {
      const root = { name: "root", children: [] };

      fileStructure.forEach((path) => {

        const addNum = path.additions;
        const deleNum = path.deletions;
        const changeNum = path.changes;
        const parts = path.filename.split('/');
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
            node.addNum = addNum;
            node.deleNum = deleNum;
            node.changeNum = changeNum;
          }

          currentDir = node;
        });
      });
      const result = JSON.stringify(root, null, 2)
      console.log(result)
      return result;
  }
  }
}
</script>
<style>

.treemap {
  flex: 1; /* Equal width for both treemaps */
  margin-right: 10px; /* Adjust margin between treemaps */
}
.treemap-container {
  width: 2000px;
  height: 1000px;
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
/* Tooltip text */
.tooltip {
  display: inline-block;
}
.tooltiptext {
  visibility: hidden;
  width: 600px;
  height: 400px;
  color: #fff;
  text-align: left;
  padding: 8px 0;
  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 1;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
}
.flex-container {
  display: flex;
}
</style>