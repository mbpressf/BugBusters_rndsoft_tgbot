<template>
    <div>
      <canvas ref="chart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  
  export default {
    props: {
      labels: { type: Array, required: true },
      data: { type: Array, required: true },
      colors: { type: Array, required: true },
    },
    mounted() {
      new Chart(this.$refs.chart, {
        type: 'pie',
        data: {
          labels: this.labels,
          datasets: [
            {
              data: this.data,
              backgroundColor: this.colors,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    },
  };
  </script>
  
  <style scoped>
  canvas {
    max-width: 100%;
    max-height: 100%;
  }
  </style>
  