<template>
  <div class="app-container bg-[#f5f4f2] min-h-[100vh] p-5">
    <router-view></router-view>
  </div>
</template>

<style>
  div {
    font-family: "Poppins";
  }
  @media (min-width: 540px) and (max-width: 960px) {
    .app-container {
      zoom: 85%;
    }
  }
</style>
