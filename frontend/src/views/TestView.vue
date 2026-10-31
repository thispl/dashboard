<template>
  <div class="min-h-screen bg-slate-50 flex flex-col p-6">
    <!-- Header -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-6 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <router-link
          to="/"
          class="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-black bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Production
        </router-link>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-2xl font-bold text-slate-800">Chart Test Sandbox</h1>
            <span class="bg-amber-100 text-amber-800 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-amber-300">
              Isolated Test Mode
            </span>
          </div>
          <p class="text-sm text-slate-500 mt-0.5">
            Compare Live Excel Database Data (DocType: Monthly Progress Data) vs Existing Static .js Files.
          </p>
        </div>
      </div>

      <!-- Controls Form -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- Chart Selector -->
        <div class="flex flex-col">
          <label class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Chart Section</label>
          <select
            v-model="selectedChart"
            @change="fetchData"
            class="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <optgroup label="Maintenance">
              <option value="room_occupancy">Room Occupancy (Building Wise)</option>
              <option value="room_occupancy_typewise">Room Occupancy (Building Type Wise)</option>
              <option value="monthwise_overall_pmi_cm_wr">Overall PM / CM / WR - MonthWise</option>
              <option value="overall_scheduled_vs_accomplished">Preventive Maintenance (PM) - Subjectwise</option>
              <option value="cm_overall_scheduled_accomplished">Corrective Maintenance (CM) - Subjectwise</option>
              <option value="wr_overall_schedule">Work Request (WR) - Subjectwise</option>
              <option value="meals">Meals Summary</option>
              <option value="laundry">Laundry</option>
              <option value="catering_laundry_service">Catering & Laundry Services (Weekwise)</option>
            </optgroup>
            <optgroup label="Operations">
              <option value="water_consumption">Water Consumption - Daywise</option>
              <option value="gasoline_consumption">Gasoline Consumption - Daywise</option>
              <option value="electricity_consumption">Electricity Consumption - Daywise</option>
              <option value="sewage_water_consumption">Sewage Water Consumption - Daywise</option>
              <option value="garbage_collection">Garbage Collection - Daywise</option>
            </optgroup>
            <optgroup label="HR & Management">
              <option value="kpi_performance_measure">KPI Title & Performance</option>
              <option value="manpower_saudi_national">Total Manpower vs Saudi National</option>
              <option value="manpower_summary">Manpower Summary</option>
              <option value="manpower_details">Manpower Detail</option>
              <option value="total_activities_done">Total Activities Done</option>
            </optgroup>
            <optgroup label="Safety">
              <option value="safety">Safety - Casewise Incidents</option>
              <option value="safety_and_environment">Safety and Environment</option>
              <option value="safety_training_on">Safety Training On</option>
            </optgroup>
          </select>
        </div>

        <!-- Site -->
        <div class="flex flex-col">
          <label class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Site</label>
          <select
            v-model="selectedSite"
            @change="fetchData"
            class="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option v-for="site in sites" :key="site" :value="site">{{ site }}</option>
          </select>
        </div>

        <!-- Month -->
        <div class="flex flex-col">
          <label class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Month</label>
          <select
            v-model="selectedMonth"
            @change="fetchData"
            class="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option v-for="month in months" :key="month" :value="month">{{ month }}</option>
          </select>
        </div>

        <!-- Year -->
        <div class="flex flex-col">
          <label class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Year</label>
          <select
            v-model="selectedYear"
            @change="fetchData"
            class="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>

        <!-- Refresh Button -->
        <button
          @click="fetchData"
          :disabled="isLoading"
          class="self-end bg-black text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-800 transition flex items-center gap-1.5"
        >
          <svg v-if="isLoading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
          </svg>
          <span>Refresh Live Data</span>
        </button>
      </div>
    </div>

    <!-- Mode Selector & Status Banner -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2 bg-slate-200 p-1 rounded-lg">
        <button
          @click="viewMode = 'comparison'"
          :class="viewMode === 'comparison' ? 'bg-white shadow-sm font-semibold text-slate-900' : 'text-slate-600'"
          class="px-3 py-1 text-xs rounded-md transition"
        >
          Side-by-Side Comparison
        </button>
        <button
          @click="viewMode = 'live'"
          :class="viewMode === 'live' ? 'bg-white shadow-sm font-semibold text-slate-900' : 'text-slate-600'"
          class="px-3 py-1 text-xs rounded-md transition"
        >
          Live Database Only
        </button>
        <button
          @click="viewMode = 'static'"
          :class="viewMode === 'static' ? 'bg-white shadow-sm font-semibold text-slate-900' : 'text-slate-600'"
          class="px-3 py-1 text-xs rounded-md transition"
        >
          Static .js Only
        </button>
      </div>

      <div class="text-xs text-slate-500">
        Active Target: <span class="font-bold text-slate-800">{{ selectedSite }} - {{ selectedMonth }} {{ selectedYear }}</span>
      </div>
    </div>

    <!-- Main Comparison Grid -->
    <div
      class="grid gap-6 flex-1"
      :class="viewMode === 'comparison' ? 'grid-cols-1 xl:grid-cols-2' : 'grid-cols-1'"
    >
      <!-- LEFT: Live Database Chart -->
      <div
        v-if="viewMode === 'comparison' || viewMode === 'live'"
        class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 flex flex-col"
      >
        <div class="flex items-center justify-between border-b pb-3 mb-4">
          <div class="flex items-center gap-2">
            <span class="inline-block w-3 h-3 rounded-full bg-emerald-500"></span>
            <h2 class="font-bold text-slate-800 text-lg">Live Database (Monthly Progress Data)</h2>
          </div>
          <span
            v-if="liveDocName"
            class="bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs px-2.5 py-1 rounded-md font-mono"
          >
            {{ liveDocName }}
          </span>
          <span
            v-else
            class="bg-amber-50 text-amber-700 border border-amber-200 text-xs px-2.5 py-1 rounded-md"
          >
            No DB Record
          </span>
        </div>

        <!-- Live Content Area -->
        <div class="flex-1 flex flex-col justify-center">
          <!-- When Live Data Exists -->
          <div v-if="liveData && liveData.length">
            <!-- 1. Room Occupancy -->
            <div v-if="selectedChart === 'room_occupancy'">
              <LineColumnChart :key="'live-occupancy-' + chartKey" :chartData="liveData[0]" />
            </div>

            <!-- 2. Room Occupancy Typewise -->
            <div v-else-if="selectedChart === 'room_occupancy_typewise'">
              <StackedAreaMixed :key="'live-occtype-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 3. Monthwise Overall PM / CM / WR -->
            <div v-else-if="selectedChart === 'monthwise_overall_pmi_cm_wr'">
              <MultiLineChart :key="'live-multiline-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 4. PM Scheduled vs Accomplished -->
            <div v-else-if="selectedChart === 'overall_scheduled_vs_accomplished'">
              <div v-if="liveData[0] && liveData[0].series">
                <div v-if="liveData[0].completion_rate" class="mb-3 text-xs font-semibold text-slate-600 flex items-center gap-2">
                  <span>PM Completion Rate:</span>
                  <span class="text-emerald-700 font-bold bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded">{{ liveData[0].completion_rate }}</span>
                </div>
                <StackedBarChart
                  :key="'live-pm-' + chartKey"
                  :chartData="liveData[0].series"
                  :categories="liveData[0].categories"
                  title=""
                />
              </div>
            </div>

            <!-- 5. CM Scheduled vs Accomplished -->
            <div v-else-if="selectedChart === 'cm_overall_scheduled_accomplished'">
              <ParetoVerticalBarChart :key="'live-cm-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 6. WR Overall Schedule -->
            <div v-else-if="selectedChart === 'wr_overall_schedule'">
              <TornadoChart :key="'live-wr-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 7. Meals Summary -->
            <div v-else-if="selectedChart === 'meals'">
              <DonutChart :key="'live-meals-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 8. Laundry -->
            <div v-else-if="selectedChart === 'laundry'" class="flex items-center justify-center p-8 bg-slate-50 border rounded-xl max-w-sm mx-auto">
              <div class="text-center">
                <div class="text-5xl font-extrabold text-slate-800">{{ liveData[0] ? liveData[0].data : 0 }}</div>
                <div class="text-xs font-semibold uppercase tracking-wider text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full mt-3 inline-block">
                  Laundry Trips
                </div>
              </div>
            </div>

            <!-- 9. Catering & Laundry Services (Weekwise) -->
            <div v-else-if="selectedChart === 'catering_laundry_service'">
              <SlopeChart :key="'live-slope-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 10. Water Consumption -->
            <div v-else-if="selectedChart === 'water_consumption'">
              <DashedLineChart :key="'live-water-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 11. Gasoline Consumption -->
            <div v-else-if="selectedChart === 'gasoline_consumption'">
              <StackedAreaChart :key="'live-gasoline-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 12. Electricity Consumption -->
            <div v-else-if="selectedChart === 'electricity_consumption'">
              <ElectricityAreaChart :key="'live-electricity-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 13. Sewage Water Consumption -->
            <div v-else-if="selectedChart === 'sewage_water_consumption'">
              <StepLineChart :key="'live-sewage-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 14. Garbage Collection -->
            <div v-else-if="selectedChart === 'garbage_collection'">
              <LineTimeSeriesChart :key="'live-garbage-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 15. KPI Chart & Detail Table -->
            <div v-else-if="selectedChart === 'kpi_performance_measure'" class="flex flex-col gap-4">
              <RadarChart :key="'live-kpi-' + chartKey" :chartData="liveData" />
              <div class="overflow-x-auto mt-2">
                <table class="w-full text-left text-sm border">
                  <thead class="bg-slate-100 text-xs font-semibold text-slate-600 uppercase">
                    <tr>
                      <th class="p-2 border">KPI Title</th>
                      <th class="p-2 border text-right">Performance Measure</th>
                      <th class="p-2 border text-right">Achieved</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(row, idx) in liveData" :key="idx" class="border-b hover:bg-slate-50 text-xs">
                      <td class="p-2 border font-medium">{{ row.title }}</td>
                      <td class="p-2 border text-right">{{ row.performanceMeasure }}%</td>
                      <td class="p-2 border text-right font-semibold text-emerald-600">{{ row.achieved }}%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 16. Total Manpower vs Saudi National -->
            <div v-else-if="selectedChart === 'manpower_saudi_national'" class="flex flex-col items-center gap-4">
              <SemiCircleGauge
                v-if="liveData[0]"
                :key="'live-gauge-' + chartKey"
                :total="liveData[0].total_sum"
                :saudi="liveData[0].nationals_sum"
              />
              <div v-if="liveData[0]" class="flex gap-4 text-xs">
                <span class="bg-slate-100 px-3 py-1.5 rounded-lg border">Total: <strong>{{ liveData[0].total_sum }}</strong></span>
                <span class="bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-lg border border-emerald-200">Saudi Nationals: <strong>{{ liveData[0].nationals_sum }}</strong></span>
              </div>
            </div>

            <!-- 17. Manpower Summary -->
            <div v-else-if="selectedChart === 'manpower_summary'">
              <BulletChart :key="'live-bullet-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 18. Manpower Details -->
            <div v-else-if="selectedChart === 'manpower_details'">
              <LineLableChart :key="'live-mandet-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 19. Safety Casewise -->
            <div v-else-if="selectedChart === 'safety'">
              <PolarAreaChart :key="'live-safety-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 20. Safety and Environment -->
            <div v-else-if="selectedChart === 'safety_and_environment'">
              <HeatMapChart :key="'live-heat-' + chartKey" :chartData="liveData" title="" />
            </div>

            <!-- 21. Safety Training On -->
            <div v-else-if="selectedChart === 'safety_training_on'">
              <HorizontalBarChart :key="'live-training-' + chartKey" :chartData="liveData" />
            </div>

            <!-- 22. Total Activities Done -->
            <div v-else-if="selectedChart === 'total_activities_done'">
              <TotalWorkChart :key="'live-totalact-' + chartKey" :chartData="liveData" />
            </div>
          </div>

          <!-- When No Live Data Found -->
          <div v-else class="text-center py-16 px-4 bg-slate-50 rounded-lg border-2 border-dashed border-slate-200">
            <svg class="mx-auto h-12 w-12 text-slate-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 class="text-base font-semibold text-slate-700">No Live Database Record Found</h3>
            <p class="text-sm text-slate-500 max-w-sm mx-auto mt-1">
              There is no <code class="bg-slate-200 px-1 rounded text-xs">Monthly Progress Data</code> document in MariaDB for 
              <strong>{{ selectedSite }} ({{ selectedMonth }} {{ selectedYear }})</strong>.
            </p>
            <p class="text-xs text-slate-400 mt-3">
              Upload an Excel file in Desk (<a href="/app/monthly-progress-upload" target="_blank" class="text-blue-600 underline">Monthly Progress Upload</a>) to populate live database values.
            </p>
          </div>
        </div>

        <!-- Raw JSON Toggle -->
        <div class="mt-4 pt-3 border-t">
          <button
            @click="showLiveJson = !showLiveJson"
            class="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1 font-mono"
          >
            <span>{{ showLiveJson ? '▼ Hide' : '▶ View' }} Live JSON Response</span>
          </button>
          <pre
            v-if="showLiveJson"
            class="mt-2 bg-slate-900 text-slate-100 p-3 rounded-lg text-xs overflow-x-auto max-h-56"
          >{{ JSON.stringify(liveData, null, 2) }}</pre>
        </div>
      </div>

      <!-- RIGHT: Static .js Chart -->
      <div
        v-if="viewMode === 'comparison' || viewMode === 'static'"
        class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 flex flex-col"
      >
        <div class="flex items-center justify-between border-b pb-3 mb-4">
          <div class="flex items-center gap-2">
            <span class="inline-block w-3 h-3 rounded-full bg-amber-500"></span>
            <h2 class="font-bold text-slate-800 text-lg">Static .js File (Original Code)</h2>
          </div>
          <span
            v-if="staticData && staticData.length"
            class="bg-amber-50 text-amber-700 border border-amber-200 text-xs px-2.5 py-1 rounded-md font-mono"
          >
            Matching Records: {{ staticData.length }}
          </span>
          <span
            v-else
            class="bg-slate-100 text-slate-500 text-xs px-2.5 py-1 rounded-md"
          >
            No JS Entry
          </span>
        </div>

        <!-- Static Content Area -->
        <div class="flex-1 flex flex-col justify-center">
          <!-- When Static Data Exists -->
          <div v-if="staticData && staticData.length">
            <!-- 1. Room Occupancy -->
            <div v-if="selectedChart === 'room_occupancy'">
              <LineColumnChart :key="'static-occupancy-' + chartKey" :chartData="staticData[0]" />
            </div>

            <!-- 2. Room Occupancy Typewise -->
            <div v-else-if="selectedChart === 'room_occupancy_typewise'">
              <StackedAreaMixed :key="'static-occtype-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 3. Monthwise Overall PM / CM / WR -->
            <div v-else-if="selectedChart === 'monthwise_overall_pmi_cm_wr'">
              <MultiLineChart :key="'static-multiline-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 4. PM Scheduled vs Accomplished -->
            <div v-else-if="selectedChart === 'overall_scheduled_vs_accomplished'">
              <div v-if="staticData[0] && staticData[0].series">
                <div v-if="staticData[0].completion_rate" class="mb-3 text-xs font-semibold text-slate-600 flex items-center gap-2">
                  <span>PM Completion Rate:</span>
                  <span class="text-amber-700 font-bold bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">{{ staticData[0].completion_rate }}</span>
                </div>
                <StackedBarChart
                  :key="'static-pm-' + chartKey"
                  :chartData="staticData[0].series"
                  :categories="staticData[0].categories"
                  title=""
                />
              </div>
            </div>

            <!-- 5. CM Scheduled vs Accomplished -->
            <div v-else-if="selectedChart === 'cm_overall_scheduled_accomplished'">
              <ParetoVerticalBarChart :key="'static-cm-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 6. WR Overall Schedule -->
            <div v-else-if="selectedChart === 'wr_overall_schedule'">
              <TornadoChart :key="'static-wr-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 7. Meals Summary -->
            <div v-else-if="selectedChart === 'meals'">
              <DonutChart :key="'static-meals-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 8. Laundry -->
            <div v-else-if="selectedChart === 'laundry'" class="flex items-center justify-center p-8 bg-slate-50 border rounded-xl max-w-sm mx-auto">
              <div class="text-center">
                <div class="text-5xl font-extrabold text-slate-800">{{ staticData[0] ? staticData[0].data : 0 }}</div>
                <div class="text-xs font-semibold uppercase tracking-wider text-amber-800 bg-amber-100 px-3 py-1 rounded-full mt-3 inline-block">
                  Laundry Trips
                </div>
              </div>
            </div>

            <!-- 9. Catering & Laundry Services (Weekwise) -->
            <div v-else-if="selectedChart === 'catering_laundry_service'">
              <SlopeChart :key="'static-slope-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 10. Water Consumption -->
            <div v-else-if="selectedChart === 'water_consumption'">
              <DashedLineChart :key="'static-water-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 11. Gasoline Consumption -->
            <div v-else-if="selectedChart === 'gasoline_consumption'">
              <StackedAreaChart :key="'static-gasoline-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 12. Electricity Consumption -->
            <div v-else-if="selectedChart === 'electricity_consumption'">
              <ElectricityAreaChart :key="'static-electricity-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 13. Sewage Water Consumption -->
            <div v-else-if="selectedChart === 'sewage_water_consumption'">
              <StepLineChart :key="'static-sewage-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 14. Garbage Collection -->
            <div v-else-if="selectedChart === 'garbage_collection'">
              <LineTimeSeriesChart :key="'static-garbage-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 15. KPI Chart & Detail Table -->
            <div v-else-if="selectedChart === 'kpi_performance_measure'" class="flex flex-col gap-4">
              <RadarChart :key="'static-kpi-' + chartKey + '-' + selectedSite + '-' + selectedMonth" :chartData="staticData" />
              <div class="overflow-x-auto mt-2">
                <table class="w-full text-left text-sm border">
                  <thead class="bg-slate-100 text-xs font-semibold text-slate-600 uppercase">
                    <tr>
                      <th class="p-2 border">KPI Title</th>
                      <th class="p-2 border text-right">Performance Measure</th>
                      <th class="p-2 border text-right">Achieved</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(row, idx) in staticData" :key="idx" class="border-b hover:bg-slate-50 text-xs">
                      <td class="p-2 border font-medium">{{ row.title }}</td>
                      <td class="p-2 border text-right">{{ row.performanceMeasure }}%</td>
                      <td class="p-2 border text-right font-semibold text-amber-600">{{ row.achieved }}%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 16. Total Manpower vs Saudi National -->
            <div v-else-if="selectedChart === 'manpower_saudi_national'" class="flex flex-col items-center gap-4">
              <SemiCircleGauge
                v-if="staticData[0]"
                :key="'static-gauge-' + chartKey"
                :total="staticData[0].total_sum"
                :saudi="staticData[0].nationals_sum"
              />
              <div v-if="staticData[0]" class="flex gap-4 text-xs">
                <span class="bg-slate-100 px-3 py-1.5 rounded-lg border">Total: <strong>{{ staticData[0].total_sum }}</strong></span>
                <span class="bg-amber-50 text-amber-800 px-3 py-1.5 rounded-lg border border-amber-200">Saudi Nationals: <strong>{{ staticData[0].nationals_sum }}</strong></span>
              </div>
            </div>

            <!-- 17. Manpower Summary -->
            <div v-else-if="selectedChart === 'manpower_summary'">
              <BulletChart :key="'static-bullet-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 18. Manpower Details -->
            <div v-else-if="selectedChart === 'manpower_details'">
              <LineLableChart :key="'static-mandet-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 19. Safety Casewise -->
            <div v-else-if="selectedChart === 'safety'">
              <PolarAreaChart :key="'static-safety-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 20. Safety and Environment -->
            <div v-else-if="selectedChart === 'safety_and_environment'">
              <HeatMapChart :key="'static-heat-' + chartKey" :chartData="staticData" title="" />
            </div>

            <!-- 21. Safety Training On -->
            <div v-else-if="selectedChart === 'safety_training_on'">
              <HorizontalBarChart :key="'static-training-' + chartKey" :chartData="staticData" />
            </div>

            <!-- 22. Total Activities Done -->
            <div v-else-if="selectedChart === 'total_activities_done'">
              <TotalWorkChart :key="'static-totalact-' + chartKey" :chartData="staticData" />
            </div>
          </div>

          <!-- When No Static Data Found -->
          <div v-else class="text-center py-16 px-4 bg-slate-50 rounded-lg border-2 border-dashed border-slate-200">
            <svg class="mx-auto h-12 w-12 text-slate-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 class="text-base font-semibold text-slate-700">No Record in .js File</h3>
            <p class="text-sm text-slate-500 max-w-sm mx-auto mt-1">
              There is no matching record in the static JS file for 
              <strong>{{ selectedSite }} ({{ selectedMonth }} {{ selectedYear }})</strong>.
            </p>
          </div>
        </div>

        <!-- Raw JSON Toggle -->
        <div class="mt-4 pt-3 border-t">
          <button
            @click="showStaticJson = !showStaticJson"
            class="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1 font-mono"
          >
            <span>{{ showStaticJson ? '▼ Hide' : '▶ View' }} Static .js Records</span>
          </button>
          <pre
            v-if="showStaticJson"
            class="mt-2 bg-slate-900 text-slate-100 p-3 rounded-lg text-xs overflow-x-auto max-h-56"
          >{{ JSON.stringify(staticData, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';

// Chart components
import LineColumnChart from '@/components/chart/LineColumnChart.vue';
import StackedAreaMixed from '@/components/chart/StackedAreaMixed.vue';
import MultiLineChart from '@/components/chart/MultiLineChart.vue';
import StackedBarChart from '@/components/chart/StackedBarChart.vue';
import ParetoVerticalBarChart from '@/components/chart/ParetoVerticalBarChart.vue';
import TornadoChart from '@/components/chart/TornadoChart.vue';
import DonutChart from '@/components/chart/DonutChart.vue';
import SlopeChart from '@/components/chart/SlopeChart.vue';
import DashedLineChart from '@/components/chart/DashedLineChart.vue';
import StackedAreaChart from '@/components/chart/StackedAreaChart.vue';
import ElectricityAreaChart from '@/components/chart/ElectricityAreaChart.vue';
import StepLineChart from '@/components/chart/StepLineChart.vue';
import LineTimeSeriesChart from '@/components/chart/LineTimeSeriesChart.vue';
import RadarChart from '@/components/chart/RadarChart.vue';
import SemiCircleGauge from '@/components/chart/SemiCircleGauge.vue';
import BulletChart from '@/components/chart/BulletChart.vue';
import LineLableChart from '@/components/chart/LineLableChart.vue';
import PolarAreaChart from '@/components/chart/PolarAreaChart.vue';
import HeatMapChart from '@/components/chart/HeatMapChart.vue';
import HorizontalBarChart from '@/components/chart/HorizontalBarChart.vue';
import TotalWorkChart from '@/components/chart/TotalWorkChart.vue';

// Static Data files (for comparison)
import staticRoomOccupancy from '@/data/maintenance/room_occupancy.js';
import staticRoomOccupancyTypewise from '@/data/maintenance/room_occupancy_typewise.js';
import staticMonthwisePmiCmWr from '@/data/maintenance/monthwise_overall_pmi_cm_wr.js';
import staticOverallSchVsAcc from '@/data/maintenance/overall_scheduled_vs_accomplished.js';
import staticCmOverall from '@/data/maintenance/cm_overall_scheduled_accomplished.js';
import staticWrOverall from '@/data/maintenance/wr_overall_schedule.js';
import staticMeals from '@/data/maintenance/meals.js';
import staticLaundry from '@/data/maintenance/laundry.js';
import staticCateringLaundry from '@/data/maintenance/catering_laundry_service.js';
import staticWaterConsumption from '@/data/maintenance/water_consumption.js';
import staticGasolineConsumption from '@/data/maintenance/gasoline_consumption.js';
import staticElectricityConsumption from '@/data/maintenance/electricity_consumption.js';
import staticSewageWater from '@/data/maintenance/sewage_water_consumption.js';
import staticGarbageCollection from '@/data/maintenance/garbage_collection.js';
import staticKpiPerformance from '@/data/maintenance/kpi_performance_measure.js';
import staticManpowerSaudi from '@/data/maintenance/manpower_saudi_national.js';
import staticManpowerSummary from '@/data/maintenance/manpower_summary.js';
import staticManpowerDetails from '@/data/maintenance/manpower_details.js';
import staticSafety from '@/data/maintenance/safety.js';
import staticSafetyEnvironment from '@/data/maintenance/safety_and_environment.js';
import staticSafetyTraining from '@/data/maintenance/safety_training_on.js';
import staticTotalActivities from '@/data/maintenance/total_activities_done.js';

export default {
  name: 'TestView',
  components: {
    LineColumnChart,
    StackedAreaMixed,
    MultiLineChart,
    StackedBarChart,
    ParetoVerticalBarChart,
    TornadoChart,
    DonutChart,
    SlopeChart,
    DashedLineChart,
    StackedAreaChart,
    ElectricityAreaChart,
    StepLineChart,
    LineTimeSeriesChart,
    RadarChart,
    SemiCircleGauge,
    BulletChart,
    LineLableChart,
    PolarAreaChart,
    HeatMapChart,
    HorizontalBarChart,
    TotalWorkChart,
  },
  setup() {
    const selectedChart = ref('room_occupancy');
    const selectedSite = ref('PS10');
    const selectedMonth = ref('September');
    const selectedYear = ref(2026);
    const viewMode = ref('comparison');

    const isLoading = ref(false);
    const liveDocName = ref(null);
    const liveData = ref(null);
    const chartKey = ref(0);

    const showLiveJson = ref(false);
    const showStaticJson = ref(false);

    const sites = ['PS10', 'PS06', 'PS03', 'PS01', 'PRS1', 'PS05'];
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    const years = [2024, 2025, 2026, 2027];

    // Static map linking dropdown key to static JS dataset
    const staticMap = {
      room_occupancy: staticRoomOccupancy,
      room_occupancy_typewise: staticRoomOccupancyTypewise,
      monthwise_overall_pmi_cm_wr: staticMonthwisePmiCmWr,
      overall_scheduled_vs_accomplished: staticOverallSchVsAcc,
      cm_overall_scheduled_accomplished: staticCmOverall,
      wr_overall_schedule: staticWrOverall,
      meals: staticMeals,
      laundry: staticLaundry,
      catering_laundry_service: staticCateringLaundry,
      water_consumption: staticWaterConsumption,
      gasoline_consumption: staticGasolineConsumption,
      electricity_consumption: staticElectricityConsumption,
      sewage_water_consumption: staticSewageWater,
      garbage_collection: staticGarbageCollection,
      kpi_performance_measure: staticKpiPerformance,
      manpower_saudi_national: staticManpowerSaudi,
      manpower_summary: staticManpowerSummary,
      manpower_details: staticManpowerDetails,
      safety: staticSafety,
      safety_and_environment: staticSafetyEnvironment,
      safety_training_on: staticSafetyTraining,
      total_activities_done: staticTotalActivities,
    };

    // Compute Static Data based on current filters
    const staticData = computed(() => {
      const dataset = staticMap[selectedChart.value] || [];

      const match = dataset.find(
        (item) =>
          item.meta &&
          item.meta.site === selectedSite.value &&
          item.meta.month === selectedMonth.value &&
          item.meta.year === selectedYear.value
      );

      return match ? match.records : [];
    });

    // Fetch live data from Frappe API endpoint
    async function fetchData() {
      isLoading.value = true;
      liveDocName.value = null;
      liveData.value = null;

      try {
        const url = `/api/method/dashboard.api.get_test_chart_data?site=${selectedSite.value}&month=${selectedMonth.value}&year=${selectedYear.value}&chart_type=${selectedChart.value}`;
        const res = await fetch(url);
        const json = await res.json();

        if (json.message && json.message.status === 'success') {
          liveDocName.value = json.message.doc_name;
          liveData.value = json.message.data;
        } else {
          liveDocName.value = null;
          liveData.value = null;
        }
      } catch (err) {
        console.error('Error fetching test chart data:', err);
        liveData.value = null;
      } finally {
        isLoading.value = false;
        chartKey.value++;
      }
    }

    onMounted(() => {
      fetchData();
    });

    return {
      selectedChart,
      selectedSite,
      selectedMonth,
      selectedYear,
      viewMode,
      isLoading,
      liveDocName,
      liveData,
      staticData,
      chartKey,
      showLiveJson,
      showStaticJson,
      sites,
      months,
      years,
      fetchData,
    };
  },
};
</script>