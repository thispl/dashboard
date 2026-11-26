<template>
  <apexchart
    type="line"
    height="500"
    :options="chartOptions"
    :series="series"
  />
</template>

<script>
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
import staffingData from "@/data/maintenance/manpower_details.js"; 

export default {
  name: "StaffingLineChart",
  components: { apexchart: VueApexCharts },
   props: {
    chartData: {
      type: Array,
      required: true
    }
  },

  setup(props) {
    const series = ref(props.chartData[0].series);

    const chartOptions = ref({
      chart: {
        height: 500,
        type: "line",
        zoom: { enabled: false },
        toolbar: { show: true }
      },

      colors: ["#77B6EA", "#545454"],

      dataLabels: {
        enabled: true
      },

      stroke: {
        curve: "smooth",
        width: 3
      },

      title: {
        text: "Indicative vs Actual Staffing",
        align: "left"
      },

      grid: {
        borderColor: "#e7e7e7",
        row: {
          colors: ["#f3f3f3", "transparent"],
          opacity: 0.5
        }
      },

      markers: {
        size: 3
      },

      xaxis: {
        categories: props.chartData[0].categories,
        tickAmount: props.chartData[0].categories.length,
        title: {
          text: "Function"
        },
        labels: {
          rotate: -45,
          style: { fontSize: "8px" }
        }
      },

      yaxis: {
        title: {
          text: "Headcount"
        }
      },

      legend: {
        position: "bottom",
        horizontalAlign: "center"
      }
    });

    return { series, chartOptions };
  }
};
</script>

<style>
/* Optional: make chart scroll if x-labels overflow */
.apexcharts-svg {
  overflow: visible !important;
}
</style>
