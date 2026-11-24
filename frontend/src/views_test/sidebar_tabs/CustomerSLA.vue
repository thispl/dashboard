<template>
  <!-- Tabs -->
  <div class="bg-white flex flex-nowrap gap-2 justify-center overflow-x-auto items-center">
    <button @click="activeTab='Maintenance'" class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Maintenance' }">
      Maintenance
    </button @click="activeTab">
    <p>|</p>
    <button @click="activeTab='Job Planning'" class="font-semibold w-full text-sm text-center h-8 pt-1 px-2"
      :class="{'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Job Planning' }">
      Job Planning
    </button @click="activeTab">
  </div>
  <!-- Charts -->
   
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'Maintenance',
    };
  }
};
</script>
