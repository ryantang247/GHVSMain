<template>
  <div ref="treeMap"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'TreeMap',
  props: {
    treeMap: {
      type: String,
    },
  },
  data() {
    return {
      data: this.treeMap,
    };
  },
  mounted() {
    this.drawTreeMap();
  },
  methods: {
    drawTreeMap() {
      const width = 500;
      const height = 300;

      const treemap = d3
          .treemap()
          .size([width, height])
          .padding(1);

      const color = d3.scaleOrdinal(d3.schemeCategory10);

      const svg = d3
          .select(this.$refs.treeMap)
          .append('svg')
          .attr('width', width)
          .attr('height', height);

      const root = d3.hierarchy(JSON.parse(this.treeMap))
          .sum(d => d.value)
          .sort((a, b) => b.value - a.value);

      treemap(root);

      svg
          .selectAll('rect')
          .data(root.leaves())
          .enter()
          .append('rect')
          .attr('x', d => d.x0)
          .attr('y', d => d.y0)
          .attr('width', d => d.x1 - d.x0)
          .attr('height', d => d.y1 - d.y0)
          .style('fill', d => color(d.parent.data.name));

    },
  },
};
</script>
