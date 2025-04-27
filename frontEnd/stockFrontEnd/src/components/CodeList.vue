<template>
  <div>
    <!-- 加载状态提示 -->
    <div v-if="loading">加载中...</div>

    <!-- 错误提示 -->
    <div v-if="error" style="color: red">{{ error }}</div>

    <select v-model="strategy" @change="fetchData">
      选股策略
      <option value="weightedScore">加权平均模型</option>
      <option value="ranking">LambdaMART模型</option>
    </select>
    <!-- 列表展示 -->
    <ul v-if="!loading && !error">
      <li
        v-for="(item, index) in items"
        :key="item"
        @click="selectItem(item)"
        :class="{ active: selectedItem === item }"
      >
        Rank: {{ index + 1 }} Code: {{ item }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [], // 列表数据
      loading: false, // 加载状态
      strategy: "ranking",
      error: null, // 错误信息
      selectedItem: null, // 选中的项
    };
  },
  async created() {
    // 组件创建时自动加载数据
    this.fetchData();
  },
  methods: {
    async getTop20Code(strategy) {
      let codeList = [];
      const options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour12: false,
      };
      const url = `http://localhost:2425/api/getTopK/20/${strategy}`;
      const startTime = Date.now();
      console.log("开始从数据库获取Top20数据...");
      console.log(url);
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("网络响应异常");
        const charDataset = await response.json();
        codeList = charDataset.code;
      } catch (error) {
        console.error("数据获取失败:", error);
      }
      const endTime = Date.now();
      console.log(`数据获取耗时: ${(endTime - startTime) / 1e3}s`);
      // console.log(codeList);
      return codeList;
    },
    async fetchData() {
      try {
        this.loading = true;

        this.getTop20Code(this.strategy).then((codeList) => {
          this.items = codeList;
        });
        console.log(this.items);
      } catch (err) {
        this.error = "数据加载失败：" + err.message;
      } finally {
        this.loading = false;
      }
    },
    selectItem(item) {
      this.selectedItem = item;
      this.$emit("item-selected", item);
    },
  },
};
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 1px 7px;
  cursor: pointer;
  border: 0.5px solid #000000;
  margin: 0 0;
}

li:hover {
  background-color: #f5f5f5;
}

li.active {
  background-color: #e0f0ff;
  border-color: #007bff;
}
</style>
