"""
命令行入口模块
"""

import argparse
import os
import sys
import webbrowser
import threading
import time
from .parser import CodeParser
from .graph_builder import GraphBuilder
from .server import run_server


def parse_args():
    parser = argparse.ArgumentParser(description="CodeGraph-Explorer - 轻量化代码结构可视化与导航工具")
    parser.add_argument('path', nargs='?', help='项目路径')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Web服务端口 (默认: 5000)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Web服务主机 (默认: 0.0.0.0)')
    parser.add_argument('--no-open', action='store_true', help='不自动打开浏览器')
    parser.add_argument('--export', '-e', type=str, help='导出图谱为JSON文件')
    parser.add_argument('--format', '-f', choices=['d3', 'cytoscape', 'json'], default='d3', help='导出格式')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0.0')
    return parser.parse_args()


def export_graph(project_path: str, output_path: str, format_type: str):
    print(f"🔍 正在解析项目: {project_path}")
    parser = CodeParser()
    parse_result = parser.parse_directory(project_path)
    graph_builder = GraphBuilder(parse_result)
    import json
    if format_type == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parse_result, f, indent=2, ensure_ascii=False)
    else:
        data = graph_builder.export_for_d3() if format_type == 'd3' else graph_builder.export_for_cytoscape()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ 图谱已导出至: {output_path}")


def start_browser(url: str):
    time.sleep(2)
    webbrowser.open(url)


def main():
    args = parse_args()
    if args.export:
        if not args.path:
            print("❌ 导出模式需要指定项目路径")
            sys.exit(1)
        if not os.path.exists(args.path):
            print(f"❌ 路径不存在: {args.path}")
            sys.exit(1)
        output_file = args.export if args.export.endswith('.json') else args.export + '.json'
        export_graph(args.path, output_file, args.format)
        return
    if not args.path:
        print("CodeGraph-Explorer v1.0.0 - 轻量化代码结构可视化工具\n使用: python main.py /path/to/project")
        sys.exit(0)
    if not os.path.exists(args.path):
        print(f"❌ 路径不存在: {args.path}")
        sys.exit(1)
    print("🔍 CodeGraph-Explorer v1.0.0")
    print(f"📁 项目路径: {args.path}")
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print("📊 正在解析代码...")
    try:
        parser = CodeParser()
        parse_result = parser.parse_directory(args.path)
        graph_builder = GraphBuilder(parse_result)
        stats = graph_builder.get_statistics()
        print(f"\n📈 解析完成! 节点:{stats['total_nodes']} 边:{stats['total_edges']} 文件:{stats['files_count']}")
        if not args.no_open:
            browser_thread = threading.Thread(target=start_browser, args=(f"http://localhost:{args.port}",))
            browser_thread.daemon = True
            browser_thread.start()
        run_server(host=args.host, port=args.port, debug=False)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
