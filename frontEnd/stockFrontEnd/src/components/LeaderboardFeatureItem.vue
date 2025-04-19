<template>
  <div class="chart-container">
    <h1><slot></slot></h1>
    <div ref="chart" class="chart"></div>
  </div>
</template>
<style>
.chart-container {
  position: relative;
  width: 100%;
  height: 900px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
<script setup>
import { defineProps, onMounted, ref, watch, watchEffect } from "vue";
import * as echarts from "echarts";
const props = defineProps(["feature", "stockCode"]);
const chart = ref(null);
let myChart = null;
// 初始化图表
const initChart = () => {
  if (chart.value) {
    myChart = echarts.init(chart.value);
    const option = {
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: "none",
          },
          brush: {
            type: ["lineX", "clear"],
          },
        },
      },
      brush: {
        xAxisIndex: "all",
        brushLink: "all",
        outOfBrush: {
          colorAlpha: 0.1,
        },
      },
      dataZoom: [
        {
          type: "inside",
          xAxisIndex: 0,
          start: 0,
          end: 20,
        },
        {
          xAxisIndex: 0,
          start: 0,
          end: 20,
        },
      ],
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "cross",
        },
        position: function (pos, params, el, elRect, size) {
          var obj = { top: 10 };
          obj[["left", "right"][+(pos[0] < size.viewSize[0] / 2)]] = 30;
          return obj;
        },
        extraCssText: "width: 170px",
      },
      axisPointer: {
        link: { xAxisIndex: "all" },
        label: {
          backgroundColor: "#777",
        },
      },
      xAxis: [
        {
          type: "category",
          name: "日期",
          scale: true,
          gridIndex: 0,
          axisLine: { onZero: false },
          splitLine: { show: false },
          axisLabel: { rotate: 50 },
          splitNumber: 20,
          min: "dataMin",
          max: "dataMax",
          boundaryGap: false,
        },
      ],
      yAxis: [
        {
          type: "value",
          scale: true,
          gridIndex: 0,
          splitArea: { show: true },
        },
      ],
      grid: [
        {
          left: "5%",
          right: "5%",
          top: "5%",
          height: "60%",
          containLabel: true,
        },
      ],
    };
    myChart.setOption(option);
  }
};

const getDataset = async (feature, stockCode) => {
  const url = `http://localhost:2425/api/getData/${feature}/${stockCode}`;
  let charDataset = [];
  const startTime = Date.now();
  console.log("开始从数据库获取数据...");
  console.log(url);
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("网络响应异常");
    charDataset = await response.json();
    charDataset.date = charDataset.date.map((p) => new Date(p).toLocaleDateString());
  } catch (error) {
    console.error("数据获取失败:", error);
  }
  const endTime = Date.now();
  console.log(`数据获取耗时: ${(endTime - startTime) / 1e3}s`);
  return charDataset;
};
// 更新图表数据
const updateChartData = async (feature, stockCode) => {
  if (!myChart) return;

  const stockDataset = await getDataset(feature, stockCode);
  const option = myChart.getOption();
  console.log(stockDataset);

  option.dataset = {
    source: stockDataset,
  };
  option.xAxis[0].data = stockDataset.date;
  const series = [];
  series.push({
    name: feature,
    type: "line",
    encode: { x: "date", y: feature },
  });
  option.series = series;
  console.log(option);

  myChart.setOption(option);
};

onMounted(() => {
  initChart();
  updateChartData(props.feature, props.stockCode);
  window.addEventListener("resize", function () {
    myChart.resize();
  });
});
watchEffect(() => {
  updateChartData(props.feature, props.stockCode);
});
</script>
