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

    /*
    * value: how large is the tree node (Eg. Value that has high revenue will have larger area of rectangle)
    *
    * */
    drawTreeMap() {
      const width = 600;
      const height = 800;

      const treemap = d3
          .treemap()
          .size([width, height])
          .padding(1);

      const color = d3.scaleLinear().range(['lightblue', 'darkblue']);
      color.domain([0, 200]);
      const svg = d3
          .select(this.$refs.treeMap)
          .append('svg')
          .attr('width', width)
          .attr('height', height);

      /*
      * Put whichever nodes that are higher first
      * */
      const root = d3.hierarchy(JSON.parse(this.treeMap))
          .sum(d => d.value)
          .sort((a, b) => b.value - a.value);

      // console.log(root)
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
          .style('fill', d => color(d.data.changeNum))

      svg
          .selectAll('text')
          .data(root.leaves())
          .enter()
          .append('text')
          .attr('x', d => d.x1 ) // Adjust the position as needed
          .attr('y', d => d.y0 ) // Adjust the position as needed
          .attr('dy', '0.7em')
          .style('text-anchor', 'end')
          .style('font-size',14)
          .text(d => d.data.name)

      svg
          .selectAll('addNum')  // Use a class for the second label
          .data(root.leaves())
          .enter()
          .append('text')
          .attr('class', 'label2')  // Add a class for the second label
          .attr('x', d => d.x1 )   // Adjust the position as needed
          .attr('y', d => d.y0 + 10 )   // Adjust the position as needed
          .attr('dy', '1em')
          .style('text-anchor', 'end')
          .style('font-size', 14)
          .text(d => "Addnum: " +d.data.addNum);

      svg
          .selectAll('delNum')  // Use a class for the second label
          .data(root.leaves())
          .enter()
          .append('text')
          .attr('class', 'label2')  // Add a class for the second label
          .attr('x', d => d.x1 )   // Adjust the position as needed
          .attr('y', d => d.y0 + 20 )   // Adjust the position as needed
          .attr('dy', '1em')
          .style('text-anchor', 'end')
          .style('font-size', 14)
          .text(d => "Delenum: " +d.data.deleNum);
      // const width = 960,
      //     height = 1060;
      //
      // const format = d3.format(",d");
      //
      // const color = d3.scaleOrdinal()
      //     .range(d3.schemeCategory10
      //         .map(function (c) {
      //           c = d3.rgb(c);
      //           c.opacity = 0.6;
      //           return c;
      //         }));
      //
      // const stratify = d3.stratify()
      //     .parentId(function (d) {
      //       return d.id.substring(0, d.id.lastIndexOf("."));
      //     });
      //
      // const treemap = d3.treemap()
      //     .size([width, height])
      //     .padding(1)
      //     .round(true);
      //
      // d3.csv("flare.csv", type, function(error, data) {
      //   if (error) throw error;
      //
      //   var root = stratify(data)
      //       .sum(function(d) { return d.value; })
      //       .sort(function(a, b) { return b.height - a.height || b.value - a.value; });
      //
      //   treemap(root);
      //
      //   d3.select("body")
      //       .selectAll(".node")
      //       .data(root.leaves())
      //       .enter().append("div")
      //       .attr("class", "node")
      //       .attr("title", function(d) { return d.id + "\n" + format(d.value); })
      //       .style("left", function(d) { return d.x0 + "px"; })
      //       .style("top", function(d) { return d.y0 + "px"; })
      //       .style("width", function(d) { return d.x1 - d.x0 + "px"; })
      //       .style("height", function(d) { return d.y1 - d.y0 + "px"; })
      //       .style("background", function(d) { while (d.depth > 1) d = d.parent; return color(d.id); })
      //       .append("div")
      //       .attr("class", "node-label")
      //       .text(function(d) { return d.id.substring(d.id.lastIndexOf(".") + 1).split(/(?=[A-Z][^A-Z])/g).join("\n"); })
      //       .append("div")
      //       .attr("class", "node-value")
      //       .text(function(d) { return format(d.value); });
      // });
    },
  },
};
</script>
