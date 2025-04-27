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

function calculateMA(dayCount, data) {
  var result = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < dayCount) {
      result.push("-");
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      sum += data[i - j];
    }
    result.push(+(sum / dayCount).toFixed(3));
  }
  return result;
}
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
          xAxisIndex: [0, 1, 2],
          start: 0,
          end: 20,
        },
        {
          xAxisIndex: [0, 1, 2],
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
        {
          type: "category",
          name: "日期",
          scale: true,
          gridIndex: 1,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          splitNumber: 20,
          min: "dataMin",
          max: "dataMax",
          boundaryGap: false,
        },
        {
          type: "category",
          name: "日期",
          scale: true,
          gridIndex: 2,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          boundaryGap: false,
        },
      ],
      yAxis: [
        {
          type: "value",
          name: "K线价格（元）",
          scale: true,
          gridIndex: 0,
          splitArea: { show: true },
        },
        {
          type: "value",
          name: "成交量（万股）",
          scale: true,
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
        },
        {
          type: "value",
          name: "成交额（万元）",
          scale: true,
          gridIndex: 2,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
        },
      ],
      grid: [
        {
          left: "10%",
          right: "5%",
          top: "5%",
          height: "40%",
          // containLabel: true,
        },
        {
          left: "10%",
          right: "5%",
          top: "55%",
          height: "15%",
          // containLabel: true,
        },
        {
          left: "10%",
          right: "5%",
          bottom: "8%",
          height: "15%",
          // containLabel: true,
        },
      ],
      series: [
        {
          name: "K线",
          type: "candlestick",
          markPoint: {
            symbol: "triangle",
            symbolSize: 10,
            data: [{ x: 100, y: 100 }],
            itemStyle: {
              color: "#ff0000",
              borderColor: "#1e0303",
            },
          },
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

  const KData = [];
  for (let i = 0; i < stockDataset.open.length; ++i) {
    KData.push([
      stockDataset.open[i],
      stockDataset.close[i],
      stockDataset.low_price[i],
      stockDataset.high_price[i],
    ]);
  }
  const buyPointsData = [];
  const sellPointsData = [];
  for (let i = 0; i < stockDataset.buyPoints.length; ++i) {
    buyPointsData.push({
      coord: [
        new Date(stockDataset.buyPoints[i]).toLocaleString("zh-CN", {
          year: "numeric",
          month: "numeric",
          day: "numeric",
          hour12: false,
        }),
        `${stockDataset.buyPointsClose[i]}`,
      ],
      symbolRotation: 0,
      itemStyle: {
        color: "#ff0000",
        borderColor: "#1e0303",
      },
    });
  }
  for (let i = 0; i < stockDataset.sellPoints.length; ++i) {
    buyPointsData.push({
      coord: [
        new Date(stockDataset.sellPoints[i]).toLocaleString("zh-CN", {
          year: "numeric",
          month: "numeric",
          day: "numeric",
          hour12: false,
        }),
        `${stockDataset.sellPointsClose[i]}`,
      ],
      symbolRotate: 180,
      itemStyle: {
        color: "#00ff00",
        borderColor: "#1e0303",
      },
    });
  }

  option.dataset = {
    source: stockDataset,
  };
  option.xAxis[0].data = stockDataset.date;
  option.xAxis[1].data = stockDataset.date;
  const series = [];
  series.push({
    name: "K线",
    type: "candlestick",
    data: KData,
    // encode: { x: "date", y: ["open", "close", "low_price", "high_price"] },
    markPoint: {
      symbol: "triangle",
      symbolSize: 10,
      data: [...buyPointsData],
    },
  });
  series.push({
    name: "MA5",
    type: "line",
    data: calculateMA(5, stockDataset.close),
    smooth: true,
    lineStyle: {
      opacity: 0.5,
    },
  });
  series.push({
    name: "MA10",
    type: "line",
    data: calculateMA(10, stockDataset.close),
    smooth: true,
    lineStyle: {
      opacity: 0.5,
    },
  });
  series.push({
    name: "MA20",
    type: "line",
    data: calculateMA(20, stockDataset.close),
    smooth: true,
    lineStyle: {
      opacity: 0.5,
    },
  });
  series.push({
    name: "Volume",
    type: "bar",
    xAxisIndex: 1,
    yAxisIndex: 1,
    encode: { x: "date", y: "volume" },
  });
  series.push({
    name: "Turnover",
    type: "bar",
    xAxisIndex: 2,
    yAxisIndex: 2,
    encode: { x: "date", y: "turnover" },
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
