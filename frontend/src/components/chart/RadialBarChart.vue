<!-- <template>
  <apexchart
    type="radialBar"
    height="350"
    :options="chartOptions"
    :series="series"
  />
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import { ref } from "vue";

export default {
  components: { apexchart: VueApexCharts },

  setup() {
    const scheduled = radialData.find(i => i.type === "Scheduled")?.value || 0;
    const accomplished = radialData.find(i => i.type === "Accomplished")?.value || 0;

    const completionRate = scheduled
      ? ((accomplished / scheduled) * 100).toFixed(0)
      : 0;

    
    const centerLabel = ref("Completion");
    const centerValue = ref(completionRate + "%");

    const series = ref([
      100,                     
      Number(completionRate)   
    ]);

    const chartOptions = ref({
      chart: {
        type: "radialBar",
        height: 350,

        events: {
          dataPointMouseEnter: (event, chartContext, config) => {
            if (config.seriesIndex === 0) {
              centerLabel.value = "Scheduled";
              centerValue.value = scheduled;
            }
            if (config.seriesIndex === 1) {
              centerLabel.value = "Accomplished";
              centerValue.value = accomplished;
            }
          },

          dataPointMouseLeave: () => {
            centerLabel.value = "Completion";
            centerValue.value = completionRate + "%";
          }
        }
      },

      labels: ["Scheduled", "Accomplished"],

      plotOptions: {
        radialBar: {
          startAngle: -135,
          endAngle: 225,

          hollow: { size: "40%" },

          dataLabels: {
            name: {
              fontSize: "16px",
              formatter: () => centerLabel.value   
            },

            value: {
              fontSize: "20px",
              fontWeight: 600,
              formatter: () => centerValue.value  
            },

            total: {
              show: true,                            
              label: "Completion",
              formatter: () => completionRate + "%"  
            }
          }
        }
      },

      colors: ["#008ffb", "#00e396"],
      stroke: { lineCap: "round" },

      tooltip: {
        enabled: true,
        y: {
          formatter: (val, opts) =>
            opts.seriesIndex === 0 ? scheduled : accomplished
        }
      }
    });

    return { series, chartOptions };
  }
};
</script> -->




  <template>
  <apexchart
    type="radialBar"
    height="350"
    :options="chartOptions"
    :series="series"
  />
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import { ref } from "vue";

export default {
  components: { apexchart: VueApexCharts },

  setup() {
    const scheduled = radialData.find(i => i.type === "Scheduled")?.value || 0;
    const accomplished = radialData.find(i => i.type === "Accomplished")?.value || 0;

    const rawValues = [scheduled, accomplished];  

    const completionRate = scheduled
      ? ((accomplished / scheduled) * 100).toFixed(0)
      : 0;

    const centerLabel = ref("Completion");
    const centerValue = ref(completionRate + "%");

    const series = ref([
      100,
      Number(completionRate)
    ]);

    const chartOptions = ref({
      chart: {
        type: "radialBar",
        height: 350,
        toolbar: { show: true },

        events: {
          

       
        dataPointMouseEnter: (event, chartContext, config) => {
        const dpIndex = config.dataPointIndex; 
        const label = config.w.config.labels[dpIndex];
        const item = radialData.find(i => i.type === label);

        centerLabel.value = item?.type || "";
        centerValue.value = item?.value || 0;
      },

          dataPointMouseLeave: () => {
            centerLabel.value = "Completion";
            centerValue.value = completionRate + "%";
          }

     



        }
      },

      labels: ["Scheduled", "Accomplished"],

      plotOptions: {
        radialBar: {
          startAngle: -135,
          endAngle: 225,

          hollow: { size: "40%" },

          dataLabels: {
            name: {
              fontSize: "16px",
              formatter: () => centerLabel.value
            },

            value: {
              fontSize: "20px",
              fontWeight: 600,
              formatter: () => centerValue.value
            },

            total: {
              show: true,
              label: "Completion",
              formatter: () => completionRate + "%"
            }
          }
        }
      },

      colors: ["#008ffb", "#00e396"],
      stroke: { lineCap: "round" },

      tooltip: {
        enabled: true,
        y: {
          formatter: (val, opts) => rawValues[opts.seriesIndex]   
        }
      }
    });

    return { series, chartOptions };
  }
};
</script>   






