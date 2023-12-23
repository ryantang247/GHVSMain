<template>
    <div>
        <select v-model="selectedOption" @change="updateChart">
            <option value="year">year</option>
            <option value="month">month</option>
            <option value="week">week</option>
            <option value="day">day</option>
        </select>
        <div id="line-chart"></div>
    </div>
</template>

<script>
import * as d3 from 'd3';
import jsondata from '../assets/data/dataline.json';

export default {
    data() {
        return {
            selectedOption: 'year',
        };
    },
    mounted() {
        this.updateChart();
    },
    methods: {
        updateChart() {
            const data = jsondata.map(item => ({
                date: new Date(item.created_at),
            }));

            const groupedData = d3.group(data, d => this.groupByOption(d.date));

            const aggregatedData = Array.from(groupedData, ([date, values]) => ({
                date,
                count: values.length,
            }));

            aggregatedData.sort((a, b) => a.date.getTime() - b.date.getTime());

            const margin = { top: 20, right: 30, bottom: 30, left: 40 };
            const width = 2000 - margin.left - margin.right;
            const height = 1000 - margin.top - margin.bottom;

            const svg = d3.select('#line-chart').html('')
                .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

            const x = d3.scaleTime().range([0, width]);
            const y = d3.scaleLinear().range([height, 0]);

            x.domain(d3.extent(aggregatedData, d => d.date));
            y.domain([0, d3.max(aggregatedData, d => d.count)]);

            // Add the line
            const line = d3.line()
                .x(d => x(d.date))
                .y(d => y(d.count));


            svg.append('path')
                .data([aggregatedData])
                .attr('class', 'line')
                .attr('d', line);

            svg.append('g')
                .attr('transform', 'translate(0,' + height + ')')
                .call(
                    d3.axisBottom(x)
                        .ticks(this.getTicks())
                        .tickFormat(d3.timeFormat(this.getFormat()))
                );

            svg.append('g')
                .call(d3.axisLeft(y));

            svg.selectAll('.dot')
                .data(aggregatedData)
                .enter().append('circle')
                .attr('class', 'dot')
                .attr('cx', d => x(d.date))
                .attr('cy', d => y(d.count))
                .attr('r', 3)
                .on('click', this.handlePointClick);  // 添加点击事件监听器

            const barWidth = 20;
            svg.selectAll('.bar')
                .data(aggregatedData)
                .enter().append('rect')
                .attr('class', 'bar')
                .attr('x', d => x(d.date) - barWidth / 2)
                .attr('y', d => y(d.count))
                .attr('width', barWidth)
                .attr('height', d => height - y(d.count));
        },
        groupByOption(date) {
            switch (this.selectedOption) {
                case 'year':
                    return d3.timeYear(date);
                case 'month':
                    return d3.timeMonth(date);
                case 'week':
                    return d3.timeWeek(date);
                case 'day':
                    return d3.timeDay(date);
                default:
                    return d3.timeYear(date);
            }
        },
        getTicks() {
            switch (this.selectedOption) {
                case 'year':
                    return d3.timeYear.every(1);
                case 'month':
                    return d3.timeMonth.every(1);
                case 'week':
                    return d3.timeWeek.every(1);
                case 'day':
                    return d3.timeDay.every(1);
                default:
                    return d3.timeYear.every(1);
            }
        },
        getFormat() {
            switch (this.selectedOption) {
                case 'year':
                    return '%Y';
                case 'month':
                    return '%Y-%m';
                case 'week':
                    return '%Y-%m-%d';
                case 'day':
                    return '%Y-%m-%d';
                default:
                    return '%Y';
            }
        },
        handlePointClick(d) {
            console.log("Clicked Point:", d);
        },

    },
};
</script>

<style>
.line {
    fill: none;
    stroke: steelblue;
    stroke-width: 2px;
}

.bar {
    fill: orange;
}

.bar:hover {
    fill: orangered;
    /* 鼠标悬停时的颜色 */
}
</style>
