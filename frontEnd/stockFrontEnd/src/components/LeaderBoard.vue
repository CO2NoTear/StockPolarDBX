<script setup>
import LeaderboardItem from "./LeaderboardItem.vue";
import { ref } from "vue";
const currentTab = ref("original");
const stockCode = ref(50);
const tabs = ["original", "SMA"];
</script>

<template>
  <div id="app">
    <div>
      <h1>股票数据看板</h1>
    </div>
    <div class="dashboard">
      <input v-model="stockCode" />
      <button
        v-for="tab in tabs"
        :key="tab"
        :class="['tab-button', { active: currentTab === tab }]"
        @click="currentTab = tab"
      >
        {{ tab }}
      </button>
      <component :is="LeaderboardItem" :feature="currentTab" :stockCode="stockCode"></component>
      <!-- <LeaderboardItem :data="chartData"></LeaderboardItem> -->
    </div>
  </div>
</template>
<style>
body {
  margin: 0;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f0f2f5;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.controls {
  margin: 20px 0;
  display: flex;
  gap: 15px;
  align-items: center;
}

button {
  padding: 8px 16px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #66b1ff;
}

.tab-button {
  padding: 6px 10px;
  color: #000000;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  border: 1px solid #ccc;
  cursor: pointer;
  background: #f0f0f0;
  margin-bottom: -1px;
  margin-right: -1px;
}

.tab-button:hover {
  color: #ffffff;
  background: #1f1e1e;
}

.tab-button.active {
  color: #ffffff;
  background: #1f1e1e;
}

input {
  padding: 6px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 100px;
}
</style>
