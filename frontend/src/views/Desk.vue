<template>
  <div class="h-[calc(100vh-40px)] flex flex-col overflow-hidden">
    <!-- Header Section -->
    <div class="bg-white flex p-5 items-center flex-shrink-0">
      <div class="flex flex-row w-full">
        <img src="../assets/icons/ACGC LOGO FULL NAME.png" class="h-10 mt-4" />
        <div class="w-full">
          <h1 class="font-semibold text-[23px] ml-[20px] mt-[5px] w-full text-center">
            Monthly Progress Observation and Analysis - {{ this.selectedMonth }} {{ this.selectedYear }}
          </h1>
          <h2 class="font-semibold text-xl ml-[20px] mt-[5px] w-full text-center opacity-50">
            {{ this.selectedSiteDescription }}
          </h2>
        </div>
      </div>

      <!-- Filter Section -->
      <div class="ml-auto flex gap-3">
        <!-- Date -->
        <!-- <input type="date" value="2025-11-12" class="border border-gray-300 rounded-md px-3 py-1 text-sm"></input>
        <input type="date" value="2025-11-12" class="border border-gray-300 rounded-md px-3 py-1 text-sm"></input> -->

        <!-- Project -->
        <!-- <input placeholder="Project" class="border border-gray-300 rounded-md px-3 py-1 text-sm"></input> -->

        <!-- Auto Switch Tabs -->
        <div class="relative group inline-block max-h-1">
          <button @click="isAutoRotateStopped = !isAutoRotateStopped">
            <svg
              class="h-8 w-8 text-[#dbdbdb] hover:opacity-75"
              :class="{ 'text-[#fba800]': isAutoRotateStopped === false }"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" />
              <path
                d="M9.828 9.172a4 4 0 1 0 0 5.656 a10 10 0 0 0 2.172 -2.828a10 10 0 0 1 2.172 -2.828 a4 4 0 1 1 0 5.656a10 10 0 0 1 -2.172 -2.828a10 10 0 0 0 -2.172 -2.828"
              />
            </svg>
          </button>

          <div
            class="absolute w-[148px] -m-12 mt-2 bg-black text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition pointer-events-none"
          >
            {{ isAutoRotateStopped ? 'Start auto switch tabs' : 'Stop auto switch tabs' }}
          </div>
        </div>
        <!-- Month -->
        <select
          v-model="selectedMonth"
          class="border border-gray-300 rounded-md px-2 py-1 text-sm w-30"
        >
          <option value="" disabled>Select an Month</option>
          <option v-for="month in months" :key="month.id" :value="month.name">
            {{ month.name }}
          </option>
        </select>

        <!-- Year -->
        <select
          v-model="selectedYear"
          class="border border-gray-300 rounded-md px-2 py-1 text-sm w-20"
        >
          <option value="" disabled>Select an Year</option>
          <option v-for="year in years" :key="year.id" :value="year.name">
            {{ year.name }}
          </option>
        </select>

        <!-- Site -->
        <select
          v-model="selectedSite"
          class="border border-gray-300 rounded-md px-2 py-1 text-sm w-20"
        >
          <option value="" disabled>Select an Site</option>
          <option v-for="site in sites" :key="site.id" :value="site.name">
            {{ site.name }}
          </option>
        </select>

        <!-- Employee -->
        <!-- <select v-model="selectedEmployee" class="border border-gray-300 rounded-md px-3 py-1 text-sm w-20">
          <option value="" disabled>Select an employee</option>
          <option
              v-for="employee in employees" :key="employee.id" :value="employee.name"
          >
              {{ employee.name }}
          </option>
        </select> -->

        <button
          type="button"
          @click="applyFilter()"
          class="bg-black text-white rounded-md px-5 py-1.5 text-sm"
        >
          Filter
        </button>
      </div>
    </div>
    <!-- Tabs Section -->
    <div class="grid grid-cols-12 gap-5 mt-5 flex-1 min-h-0" :key="gridKey">
      <div class="bg-white col-span-3 p-5 h-[45vh] overflow-y-auto">
        <h1 class="text-gray-400 font-medium">Departments</h1>
        <div>
          <!-- Management Button -->
          <router-link
            to="/management"
            @click="activeDepartment='management'"
            class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
            active-class="!border-2 !border-[#fba800] bg-[#fefdec]"
          >
            Management & Overview
            <span class="ml-auto flex items-center">
              <svg
                class="h-4 w-4 text-gray-500"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" />
                <polyline points="7 7 12 12 7 17" />
                <polyline points="13 7 18 12 13 17" />
              </svg>
            </span>
          </router-link>
          <!-- Maintenance Button -->
          <router-link
            to="/maintenance"
            @click="activeDepartment='maintenance'"
            class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
            active-class="!border-2 !border-[#fba800] bg-[#fefdec]"
          >
            Maintenance
            <span class="ml-auto flex items-center">
              <svg
                class="h-4 w-4 text-gray-500"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" />
                <polyline points="7 7 12 12 7 17" />
                <polyline points="13 7 18 12 13 17" />
              </svg>
            </span>
          </router-link>
          <!-- HR Button -->
          <router-link
            to="/hr"
            @click="activeDepartment='hr'"
            class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
            active-class="!border-2 !border-[#fba800] bg-[#fefdec]"
          >
            HR
            <span class="ml-auto flex items-center">
              <svg
                class="h-4 w-4 text-gray-500"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" />
                <polyline points="7 7 12 12 7 17" />
                <polyline points="13 7 18 12 13 17" />
              </svg>
            </span>
          </router-link>
          <!-- Safety, health & Environment Button -->
          <router-link
            to="/safety"
            @click="activeDepartment='safety'"
            class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
            active-class="!border-2 !border-[#fba800] bg-[#fefdec]"
          >
            Safety, health & Environment
            <span class="ml-auto flex items-center">
              <svg
                class="h-4 w-4 text-gray-500"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" />
                <polyline points="7 7 12 12 7 17" />
                <polyline points="13 7 18 12 13 17" />
              </svg>
            </span>
          </router-link>

          <!-- Warehouse & Procurement Button -->
          <!-- <router-link to="/warehouse" @click="activeDepartment='warehouse'" class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
              active-class="!border-2 !border-[#fba800] bg-[#fefdec]">
                  Warehouse & Procurement
                  <span class="ml-auto flex items-center">
                      <svg class="h-4 w-4 text-gray-500" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" />
                          <polyline points="7 7 12 12 7 17" />
                          <polyline points="13 7 18 12 13 17" />
                      </svg>
                  </span>
              </router-link> -->

          <!-- Customer SLA Button -->
          <!-- <router-link to="/customer-sla" @click="activeDepartment='customer'" class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
              active-class="!border-2 !border-[#fba800] bg-[#fefdec]">
                  Customer SLA
                  <span class="ml-auto flex items-center">
                      <svg class="h-4 w-4 text-gray-500" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" />
                          <polyline points="7 7 12 12 7 17" />
                          <polyline points="13 7 18 12 13 17" />
                      </svg>
                  </span>
              </router-link> -->

          <!-- Operations Button -->
          <router-link
            to="/operations"
            @click="activeDepartment='operations'"
            class="flex font-semibold px-3 py-1 mt-3 w-full border border-gray-300 text-left rounded-md transition-all duration-300 ease-in-out"
            active-class="!border-2 !border-[#fba800] bg-[#fefdec]"
          >
            Operations
            <span class="ml-auto flex items-center">
              <svg
                class="h-4 w-4 text-gray-500"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" />
                <polyline points="7 7 12 12 7 17" />
                <polyline points="13 7 18 12 13 17" />
              </svg>
            </span>
          </router-link>
        </div>
      </div>
      <div id="content-container" class="col-span-9 h-full overflow-y-auto overflow-x-hidden">
        <router-view
          :isAutoRotateStopped="isAutoRotateStopped"
          @child-cycle-complete="handleChildCycleComplete"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { useFilterStore } from '@/stores/filterStore';
import { useFilterOrgChartStore } from '@/stores/filterOrgChartStore';

export default {


  data() {
    return {
      employees: [
        { id: 1, name: "Riyaz" },
        { id: 2, name: "Amar" },
      ],
      sites: [
        // { id: "EWRC", name: "EWRC" },
        { id: "PS10", name: "PS10", description: "7006 - East West Residential Compound for PS10" },
        { id: "PS06", name: "PS06", description: "7005 - East West Residential Compound for PS06" },
        { id: "PS03", name: "PS03", description: "7003 - East West Residential Compound for PS03" },
        { id: "PS01", name: "PS01", description: "7002 - East West Residential Compound for PS01" },
        { id: "PRS1", name: "PRS1", description: "7007 - East West Residential Compound for PRS1" },
        { id: "PS05", name: "PS05", description: "7004 - East West Residential Compound for PS05" },

      ],

      months:[
        {id:1 , name:"January"},
        {id:2 , name:"February"},
        {id:3 , name:"March"},
        {id:4 , name:"April"},
        {id:5 , name:"May"},
        {id:6 , name:"June"},
        {id:7 , name:"July"},
        {id:8 , name:"August"},
        {id:9 , name:"September"},
        {id:10 , name:"October"},
        {id:11 , name:"November"},
        {id:12 , name:"December"},
      ],

      years:[

      {id:2021 , name:"2021"},
      {id:2022 , name:"2022"},
      {id:2023 , name:"2023"},
      {id:2024 , name:"2024"},
      {id:2025 , name:"2025"},
      {id:2026 , name:"2026"},
      {id:2027 , name:"2027"},
      {id:2028 , name:"2028"},
      {id:2029 , name:"2029"},
      {id:2030 , name:"2030"}

      ],



      selectedEmployee: "Riyaz",
      selectedSite: "PS10",
      selectedMonth: "",
      selectedYear: "",
      gridKey: 0,

      departments: [
      { name: "management", route: "/management" },
      { name: "maintenance", route: "/maintenance" },
      { name: "hr", route: "/hr" },
      { name: "safety", route: "/safety" },
      { name: "operations", route: "/operations" }
    ],

    currentTabIndex: 0,
    isAutoRotateStopped: false,
    activeDepartment: "management",
    resumeTimeoutId: null,
    currentSiteIndex: 0,    
    };
  },
  computed: {
  selectedSiteDescription() {
    const site = this.sites.find(s => s.name === this.selectedSite);
    return site ? site.description : "";
  }
},
  created() {
    const now = new Date();
    now.setMonth(now.getMonth() - 1); // shows the previous month
    const currentMonthIndex = now.getMonth();
    const currentYearValue = now.getFullYear();

    this.selectedMonth = this.months[currentMonthIndex].name;
    this.selectedYear = currentYearValue.toString();
    this.applyFilter();
  },

    methods: {



      applyFilter() {
      const filterStore = useFilterStore();

      const filterorgchartStore = useFilterOrgChartStore();

      filterStore.setFilters({
        year: Number(this.selectedYear),
        month: this.selectedMonth,
        site: this.selectedSite
      });

      filterorgchartStore.setFilters({
        site:this.selectedSite
      })



      this.gridKey++;

    },

    handleChildCycleComplete() {
      if (this.isAutoRotateStopped) return;

      this.currentTabIndex++;

      // ✅ Parent cycle completed
      if (this.currentTabIndex >= this.departments.length) {
        this.currentTabIndex = 0;

        // 🔁 Change Site here
        this.currentSiteIndex++;

        if (this.currentSiteIndex >= this.sites.length) {
          this.currentSiteIndex = 0;
        }

        this.selectedSite = this.sites[this.currentSiteIndex].name;

        // Apply filter after site change
        this.applyFilter();
      }

      const current = this.departments[this.currentTabIndex];

      this.activeDepartment = current.name;
      this.$router.push(current.route);
    }



  }


};
</script>

<style scoped>
option {
  width: 10px;
}
</style>
