<script setup>
import LeaderboardOriginalItem from "./LeaderboardOriginalItem.vue";
import LeaderboardFeatureItem from "./LeaderboardFeatureItem.vue";
import CodeList from "./CodeList.vue";
import { ref } from "vue";
const currentTab = ref("原始数据");
const stockCode = ref(1);
const codeList = ref([2333]);
const tabs = [
  "原始数据",
  "SMA20",
  "5日回归收益率",
  "相对强弱指数RSI",
  "指数移动线",
  "指数信号线",
  "指数柱形图",
  "布林带上轨",
  "布林带下轨",
  "成交量20日移动线",
  "市盈率分位数",
];
const LeaderboardComponentMap = {
  原始数据: LeaderboardOriginalItem,
  SMA20: LeaderboardFeatureItem,
  "5日回归收益率": LeaderboardFeatureItem,
  相对强弱指数RSI: LeaderboardFeatureItem,
  指数移动线: LeaderboardFeatureItem,
  指数信号线: LeaderboardFeatureItem,
  指数柱形图: LeaderboardFeatureItem,
  布林带上轨: LeaderboardFeatureItem,
  布林带下轨: LeaderboardFeatureItem,
  成交量20日移动线: LeaderboardFeatureItem,
  市盈率分位数: LeaderboardFeatureItem,
};
const tabsMap = {
  原始数据: "original",
  SMA20: "SMA_20",
  "5日回归收益率": "5d_Return",
  相对强弱指数RSI: "RSI",
  指数移动线: "MACD",
  指数信号线: "MACD_Signal",
  指数柱形图: "MACD_Hist",
  布林带上轨: "Bollinger_Upper",
  布林带下轨: "Bollinger_Lower",
  成交量20日移动线: "Volume_MA_20",
  市盈率分位数: "PE_Pct",
};
</script>

<template>
  <div id="app">
    <div class="dashboard">
      <form @submit.prevent="onSubmit">
        <span>股票代码</span>
        <input list="codeListOptions" v-model.lazy="stockCode" required placeholder="股票代码" />
        <span>数据类型</span>
        <select v-model.lazy="currentTab">
          <option disabled value="">请选择数据类型</option>
          <option v-for="tab in tabs" :value="tab">
            {{ tab }}
          </option>
        </select>
        <!-- <br></br> -->
        <codeList
          @item-selected="
            (item) => {
              stockCode = item;
            }
          "
        ></codeList>
        <button>确定</button>
      </form>
      <component
        :is="LeaderboardComponentMap[currentTab]"
        :feature="tabsMap[currentTab]"
        :stockCode="stockCode"
      >
        {{ currentTab }}看板
      </component>
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
h1 {
  text-align: center;
}
</style>
