# Stock PolarDB-X

## 项目介绍

- TODO

## 依赖

- See `./requirements.txt`

## Getting Started

### 1. 启动虚拟环境，安装依赖

- 使用[venv](https://docs.python.org/zh-cn/3.13/library/venv.html)
- 安装依赖
  `pip install -r ./requirements.txt`

### 2. 爬取数据

- 爬取2024年数据作为训练集
  `python -m crawlHistory -y 2024`
- 爬取2025年数据作为训练集
  `python -m crawlHistory -y 2025`

### 3. 训练一种模型，并输出对应的2025预测值

`python -m train -m ${要使用的模型名称}`

> 具体模型名称参见命令行提示内容
