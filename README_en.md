# 🔬 CodeGraph-Explorer

> 🚢 **Lightweight Code Structure Visualization & Navigation Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## 🎉 Project Introduction

**CodeGraph-Explorer** is an efficient code graph generation and visualization tool that helps developers quickly understand code structure, track call relationships, and improve code analysis efficiency.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Multi-Language Parsing** | Supports Python, JavaScript, TypeScript and more |
| 🌐 **Interactive Visualization** | Web interface displays code structure graph in real-time |
| 🔗 **Call Relationship Tracking** | Automatically analyzes function/class relationships |
| 📊 **Statistics Overview** | Provides code structure statistics |
| 💾 **Multi-Format Export** | Supports JSON, D3.js, Cytoscape.js |
| 🔎 **Fast Search** | Keyword search for quick node location |

## 🚀 Quick Start

### Requirements
- 🐍 Python 3.9+
- 🌐 Modern browser (Chrome, Firefox, Safari, Edge)

### Installation

```bash
git clone https://github.com/gitstq/CodeGraph-Explorer.git
cd CodeGraph-Explorer
pip install -r requirements.txt
```

### Usage

```bash
# Parse project and start web server
python main.py /path/to/your/project

# Specify port
python main.py /path/to/your/project --port 8080

# Export as JSON
python main.py /path/to/your/project --export output.json
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/parse` | POST | Parse project code |
| `/api/graph/cytoscape` | GET | Get graph data for Cytoscape.js |
| `/api/search?q=keyword` | GET | Search nodes |
| `/api/statistics` | GET | Get statistics |

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.9+ |
| Web Framework | Flask |
| Visualization | Cytoscape.js |
| Frontend | HTML5, CSS3, JavaScript |

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License
