<template>
  <!-- Tabs -->
  <div
    class="bg-white flex flex-nowrap gap-2 justify-center overflow-x-hidden items-center"
  >
    <button
      @click="activeTab='Overall Scheduled vs Accomplished'"
      class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Overall Scheduled vs Accomplished' }"
    >
      PM / CM / WR
    </button>
    <p>|</p>
    <button
      @click="activeTab='Catering and Laundry Services'"
      class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Catering and Laundry Services' }"
    >
      Catering and Laundry Services
    </button>
    <p>|</p>
    <button
      @click="activeTab='Room Occupancy'"
      class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Room Occupancy' }"
    >
      Room Occupancy
    </button>
  </div>

  <!-- Charts -->
  <div class="mt-4 bg-white">
    <!-- Overall Scheduled vs Accomplished -->

    <div
      v-if="activeTab =='Overall Scheduled vs Accomplished'"
      style="background-color: white"
    >
      <!-- Overall PM / CM / WR - Monthwise -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">
            Overall PM / CM / WR -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >MonthWise</span
            >
          </h1>
        </div>

        <div
          v-if="OverallMonthAllFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <MultiLineChart :chartData="OverallMonthAllFiltered" />
          </div>
        </div>
        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>

      <!-- PM Overall Scheduled vs Accomplished -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-8 mt-5 pt-5">
            Preventive Maintainance -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Subjectwise</span
            >
          </h1>
        </div>

        <div
          v-if="overallSchvsAccDataFiltered.length"
          class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"
        >
          <CountCard
            v-if="overallSchvsAccDataFiltered.length"
            :countCardData="{
                        count: overallSchvsAccDataFiltered[0].completion_rate,
                        title: 'PM Completion Rate',
                        data: overallSchvsAccDataFiltered[0].series[1].data
                    }"
          />

          <CountCard
            v-if="overallSchvsAccDataFiltered.length"
            :countCardData="{
                        count: overallSchvsAccDataFiltered[0].totals.Planned,
                        title: 'PM Planned Total',
                        data: overallSchvsAccDataFiltered[0].series[0].data
                    }"
          />

          <CountCard
            v-if="overallSchvsAccDataFiltered.length"
            :countCardData="{
                        count: overallSchvsAccDataFiltered[0].totals.Completed,
                        title: 'PM Completed Total',
                        data: overallSchvsAccDataFiltered[0].series[1].data
                    }"
          />
        </div>

        <StackedBarChart
          v-if="overallSchvsAccDataFiltered.length && overallSchvsAccDataFiltered[0].series"
          :chartData="overallSchvsAccDataFiltered[0].series"
          :categories="overallSchvsAccDataFiltered[0].categories"
          title=""
        />

        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>

      <!-- CM Overall Scheduled vs Accomplished -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-8 mt-5 pt-5">
            Corrective Maintainance -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Subjectwise</span
            >
          </h1>
        </div>

        <div
          v-if="cmOverallDataFiltered.length"
          class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"
        >
          <CountCard
            :countCardData="{
                        count: cmOverallDataFiltered[0].completion_rate,
                        title: 'CM Completion Rate',
                        data: cmOverallDataFiltered[0].accomplished
                    }"
          />

          <CountCard
            :countCardData="{
                        count: cmOverallDataFiltered[0].totals.scheduled,
                        title: 'CM Scheduled Total',
                        data: cmOverallDataFiltered[0].scheduled
                    }"
          />

          <CountCard
            :countCardData="{
                        count: cmOverallDataFiltered[0].totals.accomplished,
                        title: 'CM Accomplished Total',
                        data: cmOverallDataFiltered[0].accomplished
                    }"
          />
        </div>

        <div
          v-if="cmOverallDataFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <ParetoVerticalBarChart :chartData="cmOverallDataFiltered" />
          </div>
        </div>
        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>

      <!-- WR Overall Scheduled vs Accomplished -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-8 mt-5 pt-5">
            Work Request -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Subjectwise</span
            >
          </h1>
        </div>

        <div
          v-if="wrOverallDataFiltered.length"
          class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"
        >
          <CountCard
            :countCardData="{
                        count: wrOverallDataFiltered[0].completion_rate,
                        title: 'WR Completion Rate',
                        data: wrOverallDataFiltered[0].accomplished
                    }"
          />

          <CountCard
            :countCardData="{
                        count: wrOverallDataFiltered[0].total.scheduled,
                        title: 'WR Scheduled Total',
                        data: wrOverallDataFiltered[0].scheduled
                    }"
          />

          <CountCard
            :countCardData="{
                        count: wrOverallDataFiltered[0].total.accomplished,
                        title: 'WR Accomplished Total',
                        data: wrOverallDataFiltered[0].accomplished
                    }"
          />
        </div>

        <div
          v-if="wrOverallDataFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <TornadoChart :chartData="wrOverallDataFiltered" />
          </div>
        </div>
        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>
    </div>

    <!-- Catering and Laundry Services -->

    <div
      v-if="activeTab =='Catering and Laundry Services'"
      style="background-color: white"
    >
      <!-- Feedback -->
      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mt-5 pt-5">
            Feedback -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Weekwise</span
            >
          </h1>
          <div class="flex m-5 gap-3">
            <div
              @click="activeFeedbackType = 'Service'"
              class="w-40 cursor-pointer text-center border py-1 rounded-lg font-medium"
              :class="{'border-2 border-[#fba800] bg-[#fefdec]': activeFeedbackType === 'Service' }"
            >
              Service
            </div>
            <div
              @click="activeFeedbackType = 'Quality'"
              class="w-40 cursor-pointer text-center border py-1 rounded-lg font-medium"
              :class="{'border-2 border-[#fba800] bg-[#fefdec]': activeFeedbackType === 'Quality' }"
            >
              Quality
            </div>
          </div>
        </div>

        <div class="flex gap-5 justify-center">
          <div
            v-if="activeFeedbackType=='Service'"
            class="flex flex-col gap-4 bg-[#f5f8ff] w-full"
          >
            <BarChart :chartData="serviceFeedbackDataFiltered" />
          </div>
          <div
            v-if="activeFeedbackType=='Quality'"
            class="flex flex-col gap-4 bg-[#f5f8ff] w-full"
          >
            <BarChart :chartData="qualityFeedBackDataFiltered" />
          </div>
        </div>
      </div>

      <!-- Testimonials -->
      <div>
        <div class="relative">
          <!-- Testimonials Header -->
          <div class="flex justify-center items-center pt-5">
            <img src="../assets/icons/award-ceremony-left.png" class="h-40" />
            <div class="flex flex-col items-center gap-3">
              <h1 class="text-5xl font-semibold">
                Our Happy
                <span
                  class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
                  >Residents</span
                >
              </h1>
              <p class="text-gray-400 font-medoum text-xl">
                See how our residents are rated us
              </p>
            </div>
            <img src="../assets/icons/award-ceremony-right.png" class="h-40" />
          </div>
        </div>
        <!-- Testimonials Card -->
        <div v-if="testimonialsDataFiltered.length" class="masonry ml-14">
          <TestimonialsCard
            v-for="(data, index) in testimonialsDataFiltered"
            :key="index"
            :testimonialsCardData="data"
          />
        </div>
        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>

      <!-- Meals & Laundry -->
      <div class="grid grid-cols-12 pt-5">
        <!-- Meals -->
        <div class="col-span-6">
          <h1 class="text-3xl font-semibold text-center mt-10">
            Meals
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Summary</span
            >
          </h1>

          <div class="flex justify-center mt-5">
            <DonutChart :chartData="mealsDataFiltered" />
          </div>
        </div>

        <!-- Laundry -->
        <div class="col-span-6 p-3">
          <h1 class="text-3xl font-semibold text-center mt-7">
            Laundry
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
            ></span>
          </h1>

          <div
            class="flex gap-8 shadow-lg border w-[300px;] ml-[120px;] mt-[100px] p-6"
            style="border-radius: 8px"
          >
            <div class="flex flex-col justify-start relative">
              <!-- <div>
                <img src="../assets/icons/washing-machine.png" alt="laundry" class=" w-48"/>
                </div> -->

              <div class="flex justify-start gap-3">
                <p
                  v-if="laundryDataFiltered.length && laundryDataFiltered[0].data > 0"
                  class="text-3xl font-medium"
                >
                  {{laundryDataFiltered[0].data}}
                </p>
                <p v-else class="text-3xl font-medium">0</p>

                <div
                  class="bg-gradient-to-l from-[#fba800] to-[#232f3e] shadow"
                >
                  <p class="text-3xl font-medium text-white">Trips</p>
                </div>
              </div>
              <br />
              <p class="text-sm absolute top-[40px]">Laundry</p>
            </div>

            <div>
              <img
                src="../assets/icons/laundry.png"
                alt="laundry"
                class="w-[60px;]"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Catering and Laundry Services -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mt-5 pt-5">
            Catering and Laundry Services -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Weekwise</span
            >
          </h1>
        </div>

        <div class="flex gap-5 justify-center">
          <div class="flex flex-col gap-4 w-full">
            <SlopeChart :chartData="cateringFiltered" />
          </div>
        </div>
      </div>
    </div>

    <!-- Room Occupancy  -->

    <div v-if="activeTab =='Room Occupancy'" style="background-color: white">
      <!-- Room Occupancy -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">
            Room Occupancy -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Building wise</span
            >
          </h1>
        </div>

        <div
          v-if="roomOccupancyDataFiltered.length"
          class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"
        >
          <CountCard
            v-if="roomOccupancyDataFiltered.length"
            :countCardData="{
                count: overallOccupancy,
                title: 'Overall Occupancy',
                data: this.roomOccupancyDataFiltered[0].occupancyPercent.map(item => item)
                
                }"
          />
        </div>

        <div class="flex gap-5 justify-center">
          <div class="flex flex-col gap-4 w-full">
            <LineColumnChart
              v-if="roomOccupancyDataFiltered.length"
              :chartData="roomOccupancyDataFiltered[0]"
            />
            <div v-else class="text-center mt-5 text-gray-500">
              No data available for selected filters.
            </div>
          </div>
        </div>
      </div>

      <!-- Room Occupancy - Building Type Wise-->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">
            Room Occupancy -
            <span
              class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
              >Building Type Wise</span
            >
          </h1>
        </div>

        <div
          v-if="roomOccupancyTypeDataFiltered.length"
          class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"
        >
          <CountCard
            v-if="roomOccupancyTypeDataFiltered.length"
            :countCardData="{
                count: overallOccupancytypewise,
                title: 'Overall Occupancy',
                data: roomOccupancyTypeDataFiltered.map(item => item.occupancy)
                }"
          />
        </div>

        <div class="flex gap-5 justify-center">
          <div class="flex flex-col gap-4 w-full">
            <StackedAreaMixed
              v-if="roomOccupancyTypeDataFiltered.length"
              :chartData="roomOccupancyTypeDataFiltered"
            />
            <div v-else class="text-center mt-5 text-gray-500">
              No data available for selected filters.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full" style="color: #666666; text-align: end">
      <p>Powered by <b style="color: #211a4b">TEAMPRO</b></p>
    </div>
  </div>
</template>

<script>

    import { computed } from 'vue';
    import { useFilterStore } from '@/stores/filterStore';

    import TestimonialsCard from '@/components/TestimonialsCard.vue';
    import BarChart from '@/components/chart/BarChart.vue';
    import DonutChart from '@/components/chart/DonutChart.vue';
    import HeatMapChart from '@/components/chart/HeatMapChart.vue';
    import SlopeChart from '@/components/chart/SlopeChart.vue';
    import StackedBarChart from '@/components/chart/StackedBarChart.vue';
    import DashedLineChart from '@/components/chart/DashedLineChart.vue';
    import SlopeChartBasic from '@/components/chart/SlopeChartBasic.vue';
    import StackedAreaChart from '@/components/chart/StackedAreaChart.vue';
    import PolarAreaChart from '@/components/chart/PolarAreaChart.vue';
    import LineLableChart from '@/components/chart/LineLableChart.vue';
    import LineTimeSeriesChart from '@/components/chart/LineTimeSeriesChart.vue';
    import LineMultipleYAxis from '@/components/chart/LineMultipleYAxis.vue';
    import LineColumnChart from '@/components/chart/LineColumnChart.vue';
    import SemiCircleGauge from '@/components/chart/SemiCircleGauge.vue';
    import ParetoVerticalBarChart from '@/components/chart/ParetoVerticalBarChart.vue';
    import TornadoChart from '@/components/chart/TornadoChart.vue';
    import StepLineChart from '@/components/chart/StepLineChart.vue';
    import HorizontalBarChart from '@/components/chart/HorizontalBarChart.vue';
    import BulletChart from '@/components/chart/BulletChart.vue';
    import PercentageCard from '@/components/PercentageCard.vue';
    import CountCard from '@/components/CountCard.vue';
    import RadarChart from '@/components/chart/RadarChart.vue';
    import StackedAreaMixed from '@/components/chart/StackedAreaMixed.vue';
    import MultiLineChart from '@/components/chart/MultiLineChart.vue';
    import FlowChart from '@/components/chart/FlowChart.vue';



    import testimonialsData from '@/data/maintenance/testimonials.js';
    import serviceFeedbackData from '@/data/maintenance/service_feedback';
    import qualityFeedBackData from '@/data/maintenance/quality_feedback.js';
    import mealsData from '@/data/maintenance/meals';
    import cateringLaundryData from '@/data/maintenance/catering_laundry_service.js';
    import laundryData from '@/data/maintenance/laundry.js';
    import overallSchvsAccData from '@/data/maintenance/overall_scheduled_vs_accomplished.js';
    import waterConsumption from '@/data/maintenance/water_consumption.js';
    import gasolineConsumption from '@/data/maintenance/gasoline_consumption.js';
    import safetyData from '@/data/maintenance/safety.js';
    import manpowerDetailsData from '@/data/maintenance/manpower_details.js';
    import garbageCollectionData from '@/data/maintenance/garbage_collection.js';
    import safetyEnvironmentData from '@/data/maintenance/safety_and_environment.js';
    import roomOccupancyData from '@/data/maintenance/room_occupancy.js';
    import cmOverallData from '@/data/maintenance/cm_overall_scheduled_accomplished.js';
    import wrOverallData from '@/data/maintenance/wr_overall_schedule.js';
    import sewageWaterData from '@/data/maintenance/sewage_water_consumption.js';
    import safetyTrainingOnData from '@/data/maintenance/safety_training_on.js';
    import manpowerSummaryData from '@/data/maintenance/manpower_summary.js';
    import roomOccupancyTypeData from '@/data/maintenance/room_occupancy_typewise.js';
    import OverallMonthAll from '@/data/maintenance/monthwise_overall_pmi_cm_wr.js';
    import OrganisationChartData from '@/data/maintenance/organisation_chart.js';
    import autoScrollMixin from '@/mixins/autoScrollMixin';




    export default {
      mixins: [autoScrollMixin],
  props: {
    isAutoRotateStopped: Boolean
  },
         setup() {
            const filterStore = useFilterStore();

            const cateringFiltered = computed(() =>
            filterStore.applyFilters(cateringLaundryData)
            );

            const laundryDataFiltered = computed(()=>
                filterStore.applyFilters(laundryData)
            )

            const mealsDataFiltered = computed(()=>
                filterStore.applyFilters(mealsData)
            )

            const serviceFeedbackDataFiltered = computed(()=>
                filterStore.applyFilters(serviceFeedbackData)
            )

            const qualityFeedBackDataFiltered = computed(()=>
                filterStore.applyFilters(qualityFeedBackData)
            )

            const testimonialsDataFiltered = computed(()=>
                filterStore.applyFilters(testimonialsData)
            )

            const roomOccupancyDataFiltered = computed(()=>
                filterStore.applyFilters(roomOccupancyData)
            )

            const roomOccupancyTypeDataFiltered = computed(()=>
                filterStore.applyFilters(roomOccupancyTypeData)
            )

            const OverallMonthAllFiltered = computed(()=>
                filterStore.applyFilters(OverallMonthAll)
            )

            const overallSchvsAccDataFiltered = computed(()=>
                filterStore.applyFilters(overallSchvsAccData)
            )

            const cmOverallDataFiltered = computed(()=>
                filterStore.applyFilters(cmOverallData)
            )

            const wrOverallDataFiltered = computed(()=>
                filterStore.applyFilters(wrOverallData)
            )



            return { cateringFiltered,laundryDataFiltered,mealsDataFiltered,serviceFeedbackDataFiltered,qualityFeedBackDataFiltered,testimonialsDataFiltered,roomOccupancyDataFiltered,roomOccupancyTypeDataFiltered,OverallMonthAllFiltered,overallSchvsAccDataFiltered,cmOverallDataFiltered,wrOverallDataFiltered  };
        },
        data() {
            return {
                activeTab: 'Overall Scheduled vs Accomplished',
                activeFeedbackType: 'Service',
                testimonialsData,
                serviceFeedbackData,
                qualityFeedBackData,
                mealsData,
                cateringLaundryData,
                laundryData,
                overallSchvsAccData,
                waterConsumption,
                gasolineConsumption,
                safetyData,
                garbageCollectionData,
                safetyEnvironmentData,
                roomOccupancyData,
                cmOverallData,
                wrOverallData,
                sewageWaterData,
                safetyTrainingOnData,
                manpowerSummaryData,
                roomOccupancyTypeData,
                OverallMonthAll,
                OrganisationChartData,
                tabs: [
                    'Overall Scheduled vs Accomplished',
                    'Catering and Laundry Services',
                    'Room Occupancy'
                ],
                childTabIndex: 0,
                childIntervalId: null,
                resumeTimeoutId: null,
            };
        },
        components: {
            TestimonialsCard,
            BarChart,
            DonutChart,
            HeatMapChart,
            SlopeChart,
            StackedBarChart,
            DashedLineChart,
            SlopeChartBasic,
            StackedAreaChart,
            PolarAreaChart,
            LineLableChart,
            LineTimeSeriesChart,
            LineMultipleYAxis,
            LineColumnChart,
            SemiCircleGauge,
            ParetoVerticalBarChart,
            TornadoChart,
            StepLineChart,
            HorizontalBarChart,
            BulletChart,
            PercentageCard,
            CountCard,
            RadarChart,
            StackedAreaMixed,
            MultiLineChart,
            FlowChart
        },
        computed: {
//   overallOccupancy() {
//     // const totalOccupied = this.roomOccupancyTypeData.reduce((sum, item) => sum + item.occupied, 0);
//     const totalOccupied = this.roomOccupancyDataFiltered[0].reduce((sum, item) => sum + item.occupied, 0);
//     // const totalRooms = this.roomOccupancyTypeData.reduce((sum, item) => sum + item.total, 0);
//     const totalRooms = this.roomOccupancyDataFiltered[0].reduce((sum, item) => sum + item.total, 0);
//     return ((totalOccupied / totalRooms) * 100).toFixed(0) + ' %';
//   }


  overallOccupancy() {
    console.log(this.roomOccupancyDataFiltered);

    if (!this.roomOccupancyDataFiltered.length || !this.roomOccupancyDataFiltered[0]) {
      return '0';
    }

    const data = this.roomOccupancyDataFiltered[0];


    if (!data.occupiedRooms || !data.totalRooms) {
      return '0';
    }


    const totalOccupied = data.occupiedRooms.reduce((sum, item) => sum + item, 0);
    const totalRooms = data.totalRooms.reduce((sum, item) => sum + item, 0);


    if (totalRooms === 0) {
      return '0';
    }

    console.log(((totalOccupied / totalRooms) * 100).toFixed(0) + ' %')
    return ((totalOccupied / totalRooms) * 100).toFixed(0) + ' %';

},

overallOccupancytypewise() {
    console.log(this.roomOccupancyTypeDataFiltered);


    if (!this.roomOccupancyTypeDataFiltered.length || !this.roomOccupancyTypeDataFiltered) {
      return '0';
    }

    const data = this.roomOccupancyTypeDataFiltered;

    let totalOccupied = 0;
    let totalRooms = 0;


    data.forEach(obj => {
        totalOccupied += obj.occupied;
        totalRooms += obj.total;
    });


    if (totalRooms === 0) {
      return '0';
    }


    const occupancyPercentage = ((totalOccupied / totalRooms) * 100).toFixed(0) + ' %';

    console.log(occupancyPercentage);
    return occupancyPercentage;
},


},


    };
</script>

<style scoped>
.masonry {
  columns: 3;
  /* number of columns */
  column-gap: 10px;
  /* spacing */
}

.masonry > * {
  break-inside: avoid;
  /* important */
  margin-bottom: 24px;
}
</style>
