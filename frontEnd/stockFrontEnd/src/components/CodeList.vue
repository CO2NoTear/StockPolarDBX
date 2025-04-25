<template>
  <div>
    <!-- 加载状态提示 -->
    <div v-if="loading">加载中...</div>

    <!-- 错误提示 -->
    <div v-if="error" style="color: red">{{ error }}</div>

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

    <!-- 显示选中的值 -->
    <div v-if="selectedItem">当前选中：{{ selectedItem }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [], // 列表数据
      loading: false, // 加载状态
      error: null, // 错误信息
      selectedItem: null, // 选中的项
    };
  },
  async created() {
    // 组件创建时自动加载数据
    await this.fetchData();
  },
  methods: {
    async getTop20Code(date) {
      let codeList = [];
      const options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour12: false,
      };
      const url = `http://localhost:2425/api/getTopK/20/${new Date(date).toLocaleString("zh-CN", options).replaceAll("/", "-")}`;
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

        this.getTop20Code("2025/04/01").then((codeList) => {
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
