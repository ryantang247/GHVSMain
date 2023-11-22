<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from 'd3';
import leaves from "d3-hierarchy/src/hierarchy/leaves";
export default {
  name: 'CirclePack',
  mounted() {
    this.drawChart();
  },
  props: {
    treeMap: {
      type: String,
    },
  },

  methods: {
    drawChart() {
      // Your D3.js code for circular packing goes here
      // For example, you can start with something like this:

      const width = 500;
      const height = 500;

      const pack = d3
          .pack()
          .size([width, height])
          .padding(1.5);

      // Generate hierarchy from data
      const root = d3.hierarchy(JSON.parse(this.treeMap)).sum((d) => d.value);

      // Apply the pack layout to the hierarchy
      pack(root);

      const svg = d3.select(this.$refs.chart)
          .append('svg')
          .attr('width', width)
          .attr('height', height)
          .attr('viewBox', `0 0 ${width} ${height}`)
          .attr('font-size', 10)
          .attr('font-family', 'sans-serif')
          .attr('text-anchor', 'middle');

      const node = svg.selectAll('g')
          .data(leaves(root))
          .enter().append('g')
          .attr('transform', d => `translate(${d.x + 1},${d.y + 1})`);

      node.append('circle')
          .attr('r', d => d.r)
          .attr('fill-opacity', 0.7)
          .attr('fill', 'steelblue');

      node.append('text')
          .selectAll('tspan')
          .data(d => d.data.name.split(/(?=[A-Z][^A-Z])/g))
          .enter().append('tspan')
          .attr('x', 0)
          .attr('y', (d, i, nodes) => i * 10 - nodes.length * 5)
          .text(d => d);
    },
  },
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
