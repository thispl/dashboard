<template>
  <!-- Tabs -->
  <div class="bg-white flex flex-nowrap gap-2 justify-center overflow-x-hidden items-center">
    <button @click="activeTab='Energy'" class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Energy' }">
      Energy
    </button>
    <p>|</p>
    <button @click="activeTab='Water'" class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Water' }">
      Water
    </button>
    <p>|</p>
    <button @click="activeTab='Waste'" class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Waste' }">
      Waste
    </button>
  </div>
  <!-- Charts -->
<div class="mt-4 bg-white">

  <!-- Energy -->

  <div v-if="activeTab =='Energy'" style="background-color: white;" class="pb-[5px] " >

    <!-- Gasoline Consumption -->


        
         <div>
            <div>
                <h1 class="text-3xl font-semibold text-center  mb-3 mt-5 pt-5">Gasoline Consumption - <span class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent">Daywise</span></h1>
               
                
                
                
            </div>


             <div v-if="gasolineConsumptionFiltered.length" class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10">

                <CountCard 
                    :countCardData="{
                        count: gasolineConsumptionFiltered[0].totals.gasoline91,
                        title: 'GASOLINE 91 Total',
                        data: gasolineConsumptionFiltered[0].series[0].data
                    }"
                    />

                <CountCard 
                :countCardData="{
                    count: gasolineConsumptionFiltered[0].totals.diesel,
                    title: 'Diesel Total',
                    data: gasolineConsumptionFiltered[0].series[1].data
                }"
                />    

            </div>



            <div v-if="gasolineConsumptionFiltered.length" class="flex gap-5 justify-center">
                <div  class="flex flex-col gap-4  w-full">
                    <StackedAreaChart :chartData="gasolineConsumptionFiltered"  />
                </div>
                
            </div>
            <div v-else class="text-center mt-5 text-gray-500">
                    No data available for selected filters.
                </div>
        </div>


    <!-- Electricity Daywise     -->

      <div>
            <div>
                <h1 class="text-3xl font-semibold text-center  mb-3 mt-5 pt-5">Electicity Consumption - <span class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent">Daywise</span></h1>
               
                
                
                
            </div>


             <div v-if="electricityDataFiltered.length" class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10">

                <CountCard 
                    :countCardData="{
                        count: electricityDataFiltered[0].totals.electricity,
                        title: 'Electicity Usage Total',
                        data: electricityDataFiltered[0].series[0].data
                    }"
                    />

                  

            </div>



            <div v-if="electricityDataFiltered.length" class="flex gap-5 justify-center">
                <div  class="flex flex-col gap-4  w-full">
                   <ElectricityAreaChart
                                v-if="electricityDataFiltered.length"
                                :chartData="electricityDataFiltered"
                                />
                </div>
                
            </div>
            <div v-else class="text-center mt-5 text-gray-500">
                    No data available for selected filters.
                </div>
        </div>

  </div>


  <!-- Water -->

  <div v-if="activeTab =='Water'" style="background-color: white;" class="pb-[5px]" >



     <!-- Water Consumption	 -->

          <div>
            <div>
                <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">Water Consumption - <span class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent">Daywise</span> </h1>
                
                
            </div>

            <div v-if="waterConsumptionFiltered.length" class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10">

                <CountCard 
                    :countCardData="{
                        count: waterConsumptionFiltered[0].totals.raw,
                        title: 'RAW Water Total',
                        data: waterConsumptionFiltered[0].series[0].data
                    }"
                    />

                <CountCard 
                :countCardData="{
                    count: waterConsumptionFiltered[0].totals.sweet,
                    title: 'Sweet Water Total',
                    data: waterConsumptionFiltered[0].series[1].data
                }"
                />    

            </div>


            <div class="flex gap-5 justify-center">
                <div v-if="waterConsumptionFiltered.length"  class="flex flex-col gap-4 w-full">
                    <DashedLineChart :chartData="waterConsumptionFiltered"  />
                </div>
                <div v-else class="text-center mt-5 text-gray-500">
                    No data available for selected filters.
                </div>
            </div>
        </div>



  </div>

  <!-- Waste -->

  <div v-if="activeTab =='Waste'" style="background-color: white;" class="pb-[5px]" >


    <!-- Garbage Collection -->

         
            <div>
                <h1 class="text-3xl font-semibold text-center mb-3 mt-5 pt-5">Garbage Collection - <span class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent">Daywise</span></h1> 
            </div>

            
             <div v-if="garbageCollectionDataFiltered.length > 0"  class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10"> 

                <CountCard
                :countCardData="{
                    count: garbageCollectionDataFiltered[0].totals,
                    title: 'Garbage Collection Total',
                    data: garbageCollectionDataFiltered[0].capacities
                }"
                />
  

             </div>




            <div v-if="garbageCollectionDataFiltered.length > 0" class="flex gap-5 justify-center">
            <div class="flex flex-col gap-4 w-full">
                <LineTimeSeriesChart :chartData="garbageCollectionDataFiltered" />
            </div>
            </div>

            <div v-else class="text-center mt-5 text-gray-500">
            No data available for selected filters.
            </div>



           
            






      <!-- Sewage Water Consumption-->

         <div>
            <div>
                <h1 class="text-3xl font-semibold text-center mb-3 mt-5">Sewage Water Consumption - <span class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent">Daywise</span></h1>
                
                
                
            </div>


             <div v-if="sewageWaterDataFiltered.length" class="ml-[10px] my-[20px] w-full h-[100px] flex gap-10">

                <CountCard 
                    :countCardData="{
                        count: sewageWaterDataFiltered[0].totals,
                        title: 'Sewage Water Total (In Ltrs)',
                        data: sewageWaterDataFiltered[0].capacities
                    }"
                    />
  

            </div>

            <div v-if="sewageWaterDataFiltered.length" class="flex gap-5 justify-center">
                <div  class="flex flex-col gap-4  w-full">
                    <StepLineChart :chartData="sewageWaterDataFiltered"  />
                </div>
                
            </div>
            <div v-else class="text-center mt-5 text-gray-500">
            No data available for selected filters.
            </div>
            
        </div>



  </div>

<div class="w-full" style="color:#666666; text-align:end;"><p>Powered by <b style='color:#211a4b;'>TEAMPRO</b></p></div>

</div>
   
</template>

<script>
import { computed } from 'vue';
import { useLiveFilterStore } from '@/stores/liveFilterStore';

import StepLineChart from '@/components/chart/StepLineChart.vue';
import LineTimeSeriesChart from '@/components/chart/LineTimeSeriesChart.vue';
import CountCard from '@/components/CountCard.vue';
import StackedAreaChart from '@/components/chart/StackedAreaChart.vue';
import DashedLineChart from '@/components/chart/DashedLineChart.vue';
import ElectricityAreaChart from '@/components/chart/ElectricityAreaChart.vue';
import autoScrollMixin from '@/mixins/autoScrollMixin';

export default {
  mixins: [autoScrollMixin],
  props: {
    isAutoRotateStopped: Boolean
  },

  setup() {
    const liveFilterStore = useLiveFilterStore();

    const gasolineConsumptionFiltered = computed(() =>
      liveFilterStore.getDataset('gasoline_consumption')
    );
    const waterConsumptionFiltered = computed(() =>
      liveFilterStore.getDataset('water_consumption')
    );
    const garbageCollectionDataFiltered = computed(() =>
      liveFilterStore.getDataset('garbage_collection')
    );
    const sewageWaterDataFiltered = computed(() =>
      liveFilterStore.getDataset('sewage_water_consumption')
    );
    const electricityDataFiltered = computed(() =>
      liveFilterStore.getDataset('electricity_consumption')
    );

    return {
      gasolineConsumptionFiltered,
      waterConsumptionFiltered,
      garbageCollectionDataFiltered,
      sewageWaterDataFiltered,
      electricityDataFiltered
    };
  },

  data() {
    return {
      activeTab: 'Energy',
      tabs: [
        'Energy',
        'Water',
        'Waste'
      ],
      childTabIndex: 0,
      childIntervalId: null,
      resumeTimeoutId: null,
    };
  },

  components: {
    StepLineChart,
    LineTimeSeriesChart,
    CountCard,
    StackedAreaChart,
    DashedLineChart,
    ElectricityAreaChart
  },
};
</script>
