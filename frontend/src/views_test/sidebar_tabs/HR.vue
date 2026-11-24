<template>
  <!-- Tabs -->
  <div
    class="bg-white flex flex-nowrap gap-2 justify-center overflow-x-hidden items-center"
  >
    <button
      @click="activeTab='Saudization'"
      class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Saudization' }"
    >
      Saudization
    </button>

    <p>|</p>

    <button
      @click="activeTab='Management KPI'"
      class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Management KPI' }"
    >
      Management KPI
    </button>
    <p>|</p>
    <button
      @click="activeTab='Man Power Trends'"
      class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Man Power Trends' }"
    >
      Man Power
    </button>
  </div>
  <!-- Charts -->

  <div class="mt-4 bg-white">
    <!-- Saudization -->
    <div v-if="activeTab =='Saudization'" style="background-color: white">
      <!-- Total Manpower vs Saudi National -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">
            Total Manpower vs Saudi National
          </h1>
        </div>

        <div
          v-if="manpowerSaudiNationalDataFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <SemiCircleGauge
              :total="manpowerSaudiNationalDataFiltered[0].total_sum"
              :saudi="manpowerSaudiNationalDataFiltered[0].nationals_sum"
            />
          </div>
        </div>

        <div
          v-if="manpowerSaudiNationalDataFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <RadialGauge :chartData="manpowerSaudiNationalDataFiltered" />
          </div>
        </div>
        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>
    </div>

    <!-- Management KPI -->

    <div v-if="activeTab =='Management KPI'" style="background-color: white">
      <!-- KPI Performance Measure -->
      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">
            KPI Performance Measure
          </h1>
        </div>

        <div
          v-if="kpiPerformanceMeasureFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <RadarChart :chartData="kpiPerformanceMeasureFiltered" />
          </div>
        </div>

        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>
    </div>

    <!-- Man Power Trends  -->

    <div v-if="activeTab =='Man Power Trends'" style="background-color: white">
      <!-- Manpower Summary -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">
            Manpower Summary
          </h1>
        </div>

        <div
          v-if="manpowerSummaryDataFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <BulletChart :chartData="manpowerSummaryDataFiltered" />
          </div>
        </div>
        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
        </div>
      </div>

      <!-- Manpower Detail -->

      <div>
        <div>
          <h1 class="text-3xl font-semibold text-center mb-3 mt-5">
            Manpower Detail
          </h1>
        </div>

        <div
          v-if="manpowerDetailsDataFiltered.length"
          class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"
        >
          <CountCard
            :countCardData="{
                        count: manpowerDetailsDataFiltered[0].totals.indicative,
                        title: 'Indicative Total',
                        data: manpowerDetailsDataFiltered[0].series[0].data
                    }"
          />

          <CountCard
            :countCardData="{
                    count: manpowerDetailsDataFiltered[0].totals.actual,
                    title: 'Actual Total',
                    data: manpowerDetailsDataFiltered[0].series[1].data
                }"
          />
        </div>

        <div
          v-if="manpowerDetailsDataFiltered.length"
          class="flex gap-5 justify-center"
        >
          <div class="flex flex-col gap-4 w-full">
            <LineLableChart :chartData="manpowerDetailsDataFiltered" />
          </div>
        </div>

        <div v-else class="text-center mt-5 text-gray-500">
          No data available for selected filters.
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
import { useLiveFilterStore } from '@/stores/liveFilterStore';

import SemiCircleGauge from '@/components/chart/SemiCircleGauge.vue';
import RadialGauge from '@/components/chart/RadialGauge.vue';
import RadarChart from '@/components/chart/RadarChart.vue';
import BulletChart from '@/components/chart/BulletChart.vue';
import LineLableChart from '@/components/chart/LineLableChart.vue';
import CountCard from '@/components/CountCard.vue';
import autoScrollMixin from '@/mixins/autoScrollMixin';

export default {
  mixins: [autoScrollMixin],
  props: {
    isAutoRotateStopped: Boolean
  },

  setup() {
    const liveFilterStore = useLiveFilterStore();

    const manpowerSaudiNationalDataFiltered = computed(() =>
      liveFilterStore.getDataset('manpower_saudi_national')
    );
    const kpiPerformanceMeasureFiltered = computed(() =>
      liveFilterStore.getDataset('kpi_performance_measure')
    );
    const manpowerSummaryDataFiltered = computed(() =>
      liveFilterStore.getDataset('manpower_summary')
    );
    const manpowerDetailsDataFiltered = computed(() =>
      liveFilterStore.getDataset('manpower_details')
    );

    return {
      manpowerSaudiNationalDataFiltered,
      kpiPerformanceMeasureFiltered,
      manpowerSummaryDataFiltered,
      manpowerDetailsDataFiltered
    };
  },
  data() {
    return {
      activeTab: 'Saudization',
      childIntervalId: null,
      tabs: [
        'Saudization',
        'Management KPI',
        'Man Power Trends'
      ],
      childTabIndex: 0,
      resumeTimeoutId: null,
    };
  },

  components: {
    SemiCircleGauge,
    RadialGauge,
    RadarChart,
    BulletChart,
    LineLableChart,
    CountCard
  },
};
</script>
