# 🔬 CodeGraph-Explorer

> 🚢 **輕量化程式碼結構視覺化與導航工具**

## 🎉 專案介紹

**CodeGraph-Explorer** 是一款高效的程式碼圖譜生成和視覺化工具，幫助開發者快速理解程式碼結構、追蹤呼叫關係。

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🔍 **多語言解析** | 支援 Python、JavaScript、TypeScript |
| 🌐 **互動式視覺化** | Web介面即時展示程式碼結構圖譜 |
| 🔗 **呼叫關係追蹤** | 自動分析函數/類的呼叫關係 |
| 📊 **統計概覽** | 提供程式碼結構統計資訊 |
| 💾 **多格式匯出** | 支援 JSON、Cytoscape.js |
| 🔎 **快速搜尋** | 關鍵詞搜尋快速定位節點 |

## 🚀 快速開始

### 環境要求
- 🐍 Python 3.9+
- 🌐 現代瀏覽器

### 安裝

```bash
git clone https://github.com/gitstq/CodeGraph-Explorer.git
cd CodeGraph-Explorer
pip install -r requirements.txt
```

### 使用方法

```bash
# 解析專案並啟動Web服務
python main.py /path/to/your/project

# 指定連接埠
python main.py /path/to/your/project --port 8080

# 匯出為JSON
python main.py /path/to/your/project --export output.json
```

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 開源協議

MIT License
