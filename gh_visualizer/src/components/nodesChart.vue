<template>
  <div ref="chartContainer">
    <div id="tooltip"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import data from '../assets/data_node.json';

export default {
  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      // 数据处理
      const nodes = [];
      const links = [];

      data.forEach(event => {
        // 添加作者节点，如果作者节点不存在
        if (!nodes.some(node => node.id === event.author)) {
          nodes.push({ id: event.author, group: 1 });
        }

        // 添加参与者节点和链接
        event.participants.forEach(participant => {
          // 添加参与者节点，如果节点不存在
          if (!nodes.some(node => node.id === participant)) {
            nodes.push({ id: participant, group: 2 });
          }

          // 添加链接，如果链接不存在
          if (!links.some(link => link.source === event.author && link.target === participant)) {
            links.push({ source: event.author, target: participant });
          }
        });
      });


      // 创建 SVG 容器
      const svg = d3.select(this.$refs.chartContainer)
        .append("svg")
        .attr("width", 700)
        .attr("height", 500);

      // 创建力导向图
      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(5))
        .force("charge", d3.forceManyBody().strength(-50))
        .force("center", d3.forceCenter(350, 250));

      // 绘制链接
      const link = svg.selectAll("line")
        .data(links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .attr("stroke-width", 2);

      // 绘制节点
      const node = svg.selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("r", 5)
        .attr("fill", d => (d.group === 1) ? "red" : "blue")
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);

      // 添加节点标签
      node.append("title")
        .text(d => d.id);

      // 设置力导向图的 tick 事件
      simulation.on("tick", () => {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
      });

      const drag = d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);

      node.call(drag);

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
        simulation.restart();
      }

      function handleMouseOver(event, d) {
        if (event.active) {
          console.log(d.group)
          const tooltip = d3.select("#tooltip");

          tooltip.transition()
            .duration(200)
            .style("opacity", .9);

          tooltip.html(`<strong>ID:</strong> ${d.id}`)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");

          console.log(d.group)
          // 如果是作者节点，显示相关的数据
          if (d.group === 1) {
            const authorData = this.jsondata.filter(item => item.author === d.id || item.participants.includes(d.id));
            console.log(authorData)
            tooltip.html(`<strong>ID:</strong> ${d.id} <br> <strong>Data:</strong> ${JSON.stringify(authorData)}`);
          }
        }

      }

      function handleMouseOut(event) {
        if (event.active) {
          d3.select("#tooltip").transition()
            .duration(500)
            .style("opacity", 0);
        }


      }
    },
  },
};
</script>

<style scoped>
#chartContainer {
  width: 100%;
  height: 100%;
}

#tooltip {
  position: absolute;
  text-align: left;
  padding: 10px;
  font: 12px sans-serif;
  background: #fff;
  border: 1px solid #aaa;
  border-radius: 5px;
  pointer-events: none;
  opacity: 0;
}
</style>
