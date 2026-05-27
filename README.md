# 🔬 CodeGraph-Explorer

> 🚢 **轻量化代码结构可视化与导航工具**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## 🎉 项目介绍

**CodeGraph-Explorer** 是一款高效的代码图谱生成和可视化工具，帮助开发者快速理解代码结构、追踪调用关系、提升代码分析效率。

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **多语言解析** | 支持 Python、JavaScript、TypeScript 等主流语言 |
| 🌐 **交互式可视化** | Web界面实时展示代码结构图谱 |
| 🔗 **调用关系追踪** | 自动分析函数/类的调用和被调用关系 |
| 📊 **统计概览** | 提供代码结构统计信息 |
| 💾 **多格式导出** | 支持 JSON、D3.js、Cytoscape.js 等多种格式 |
| 🔎 **快速搜索** | 关键词搜索，快速定位目标节点 |

## 🚀 快速开始

### 环境要求
- 🐍 Python 3.9+
- 🌐 现代浏览器 (Chrome、Firefox、Safari、Edge)

### 安装

```bash
git clone https://github.com/gitstq/CodeGraph-Explorer.git
cd CodeGraph-Explorer
pip install -r requirements.txt
```

### 使用方法

```bash
# 解析项目并启动Web服务
python main.py /path/to/your/project

# 指定端口
python main.py /path/to/your/project --port 8080

# 不自动打开浏览器
python main.py /path/to/your/project --no-open

# 导出为JSON
python main.py /path/to/your/project --export output.json
```

### Docker部署

```bash
docker build -t codegraph-explorer .
docker run -p 5000:5000 codegraph-explorer
```

## 📖 API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/parse` | POST | 解析项目代码 |
| `/api/graph/d3` | GET | 获取D3.js格式的图谱数据 |
| `/api/graph/cytoscape` | GET | 获取Cytoscape.js格式的图谱数据 |
| `/api/search?q=keyword` | GET | 搜索节点 |
| `/api/node/<id>` | GET | 获取节点详情 |
| `/api/statistics` | GET | 获取统计信息 |

## 📦 项目结构

```
CodeGraph-Explorer/
├── src/                    # 源代码
│   ├── parser.py          # 代码解析器
│   ├── graph_builder.py   # 图谱构建器
│   ├── server.py          # Web服务器
│   └── cli.py             # 命令行入口
├── templates/             # HTML模板
├── static/                # 静态资源
├── tests/                 # 测试用例
├── main.py               # 程序入口
└── requirements.txt       # Python依赖
```

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端核心 | Python 3.9+ |
| Web框架 | Flask |
| 可视化 | Cytoscape.js, D3.js |
| 前端 | HTML5, CSS3, JavaScript |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

本项目采用 MIT License 开源协议。

---

⭐ **如果这个项目对您有帮助，请给我们一个 Star！**
