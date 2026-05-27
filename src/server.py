"""
Flask Web服务器模块
"""

import os
from flask import Flask, render_template, request, jsonify
from .parser import CodeParser
from .graph_builder import GraphBuilder

app = Flask(__name__, template_folder='../templates', static_folder='../static')
graph_builder = None


def create_app():
    return app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/parse', methods=['POST'])
def parse_code():
    global graph_builder
    data = request.get_json()
    project_path = data.get('path', '')
    if not project_path or not os.path.exists(project_path):
        return jsonify({"error": "Invalid path"}), 400
    try:
        parser = CodeParser()
        parse_result = parser.parse_directory(project_path)
        graph_builder = GraphBuilder(parse_result)
        return jsonify({"success": True, "statistics": graph_builder.get_statistics()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graph/<format_type>')
def get_graph(format_type):
    global graph_builder
    if not graph_builder:
        return jsonify({"error": "No graph data"}), 400
    if format_type == 'd3':
        return jsonify(graph_builder.export_for_d3())
    elif format_type == 'cytoscape':
        return jsonify(graph_builder.export_for_cytoscape())
    return jsonify({"error": "Invalid format"}), 400


@app.route('/api/search', methods=['GET'])
def search_nodes():
    global graph_builder
    if not graph_builder:
        return jsonify({"error": "No graph data"}), 400
    keyword = request.args.get('q', '')
    results = graph_builder.search_nodes(keyword)
    return jsonify({"results": results})


@app.route('/api/node/<node_id>')
def get_node_detail(node_id):
    global graph_builder
    if not graph_builder:
        return jsonify({"error": "No graph data"}), 400
    node = graph_builder.get_node(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404
    dependencies = graph_builder.get_dependencies(node_id)
    dependents = graph_builder.get_dependents(node_id)
    return jsonify({"node": node, "dependencies": dependencies, "dependents": dependents})


@app.route('/api/statistics')
def get_statistics():
    global graph_builder
    if not graph_builder:
        return jsonify({"error": "No graph data"}), 400
    return jsonify(graph_builder.get_statistics())


def run_server(host='0.0.0.0', port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
