<template>
    <div ref="issueChart"></div>
</template>

<style scoped>
/* Add any necessary styling here */
</style>

<script>
import * as d3 from 'd3';
import closed_issues from '../issue_closed.json';
import {Octokit} from "@octokit/rest";
import config from "@/auth_config";

export default {
  name: 'issueChart',
  props: {
  },
  data() {
    return {
      data: closed_issues,
      time: null,
      repo: "Github-Ranking",
      author : "EvanLi",
      get_closed_merged: false
    };
  },
  mounted() {
    this.drawGraph();
  },
  methods: {
    handleTimeClick(time){
      this.time = time
    },
    async getFileContents() {
      // this.loading = true;
      const octokit = new Octokit({
        auth: config.githubToken
      })

      // const apiUrl = `https://api.github.com/repos/${this.username}/${this.repo}/contents/`;
      // https://api.github.com/search/issues?q=stress+test+label:bug+language:python+state:closed&per_page=100
      try {

        let url = ""

        if (this.get_closed_merged) {
          url = `GET https://api.github.com/repos/${this.author}/${this.repo}/issues?state=closed`;
        } else {
          url = `GET https://api.github.com/repos/${this.author}/${this.repo}/issues?state=open`;
        }

        const response = await octokit.request(url, {
          owner: this.author,
          repo: this.repo,
          page_number: 100,
          headers: {
            'Accept': 'application/vnd.github.v3.raw', // This header indicates that you want the raw content
          },
        });

        // remember to put loaded to true for passing data

        const content = response.data;

        // Processing data by getting pull requests id and puttting it in array, this is using pull id to get its respective commits
        // this.pullJSONData = response.data
        // this.pullNumbers = this.pullJSONData.map(item => item.number);
        return content;

      } catch{
        this.loading = false;
        this.error = 'Error fetching data!'
      }

    },
    drawGraph() {
      const margin = { top: 10, right: 30, bottom: 30, left: 30 },
          width = 2400 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
      const svg = d3
          .select(this.$refs.issueChart)
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // console.log(this.data)
      const data  = closed_issues;
      // d3.json(data)
      //
      //     .then((data) => {

            // Extract timestamps and convert them to Date objects
      const timestamps = data.map((issue) => ({
        created_at: new Date(issue.created_at),
        closed_at: new Date(issue.closed_at),
      }));

      const minTimestamp = d3.min(timestamps, (data) => data.created_at);
      const maxTimestamp = d3.max(timestamps, (data) => data.closed_at);

      // X axis
      const x = d3.scaleTime().domain([minTimestamp, maxTimestamp]).range([0, width]);

      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      svg.selectAll("myline")
          .data(data)
          .enter()
          .append("line")
          .attr("x1", (d) => x(new Date(d.created_at)))
          .attr("x2", (d) => x(new Date(d.closed_at)))
          .attr("y1", (d, i) => (i) * 3.5)  // Increment y by i
          .attr("y2", (d, i) => (i)* 3.5)
          .attr("stroke", "grey")
          .attr("stroke-width", "2px")
          .append("title")
          .text((d) => `Title: ${d.title}, Created: ${d.created_at}, Closed: ${d.closed_at}`);

      // Circles of variable 1
      svg.selectAll("mycircle1")
          .data(data)
          .enter()
          .append("circle")
          .attr("cx", (d) => x(new Date(d.created_at)))
          .attr("cy", (d, i) => (i)* 3.5)
          .attr("r", "6")
          .style("fill", "#69b3a2");

      // Circles of variable 2
      svg.selectAll("mycircle2")
          .data(data)
          .enter()
          .append("circle")
          .attr("cx", (d) => x(new Date(d.closed_at)))
          .attr("cy", (d, i) => (i)* 3.5)
          .attr("r", "6")
          .style("fill", "#4C4082");

      // svg.append("rect")
      //     .attr("class", "overlay")
      //     .attr("width", width)
      //     .attr("height", height)
      //     .style("fill", "none")
      //     .style("pointer-events", "all")
      //     .on("click", handleXAxisClick);
    //       })
    //       .catch((error) => {
    //         console.error("Error loading JSON data", error);
    // });
    },

  },
};
</script>
