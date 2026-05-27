"""
图谱构建器模块
"""

from typing import Dict, List, Optional
from collections import defaultdict


class GraphBuilder:
    """代码图谱构建器"""

    def __init__(self, parse_result: Dict):
        self.nodes = parse_result.get("nodes", [])
        self.edges = parse_result.get("edges", [])
        self._build_index()

    def _build_index(self) -> None:
        self.node_by_id = {node["id"]: node for node in self.nodes}
        self.nodes_by_type = defaultdict(list)
        self.nodes_by_file = defaultdict(list)
        self.adjacency = defaultdict(list)
        self.reverse_adjacency = defaultdict(list)
        for node in self.nodes:
            self.nodes_by_type[node["type"]].append(node)
            self.nodes_by_file[node.get("file_path", "")].append(node)
        for edge in self.edges:
            self.adjacency[edge["source"]].append(edge)
            self.reverse_adjacency[edge["target"]].append(edge)

    def get_node(self, node_id: str) -> Optional[Dict]:
        return self.node_by_id.get(node_id)

    def get_nodes_by_type(self, node_type: str) -> List[Dict]:
        return self.nodes_by_type.get(node_type, [])

    def get_nodes_by_file(self, file_path: str) -> List[Dict]:
        return self.nodes_by_file.get(file_path, [])

    def get_dependencies(self, node_id: str) -> List[Dict]:
        dependencies = []
        for edge in self.adjacency.get(node_id, []):
            target = self.get_node(edge["target"])
            if target:
                dependencies.append({"node": target, "relation": edge["relation"]})
        return dependencies

    def get_dependents(self, node_id: str) -> List[Dict]:
        dependents = []
        for edge in self.reverse_adjacency.get(node_id, []):
            source = self.get_node(edge["source"])
            if source:
                dependents.append({"node": source, "relation": edge["relation"]})
        return dependents

    def search_nodes(self, keyword: str, case_sensitive: bool = False) -> List[Dict]:
        results = []
        search_keyword = keyword if case_sensitive else keyword.lower()
        for node in self.nodes:
            name = node["name"] if case_sensitive else node["name"].lower()
            if search_keyword in name:
                results.append(node)
        return results

    def get_statistics(self) -> Dict:
        type_counts = defaultdict(int)
        file_counts = defaultdict(int)
        for node in self.nodes:
            type_counts[node["type"]] += 1
            file_counts[node.get("file_path", "unknown")] += 1
        return {
            "total_nodes": len(self.nodes), "total_edges": len(self.edges),
            "nodes_by_type": dict(type_counts), "files_count": len(file_counts),
            "top_files": sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }

    def export_for_d3(self) -> Dict:
        nodes = [{"id": n["id"], "name": n["name"], "type": n["type"], "group": n["type"]} for n in self.nodes]
        links = [{"source": e["source"], "target": e["target"], "relation": e["relation"]} for e in self.edges]
        return {"nodes": nodes, "links": links}

    def export_for_cytoscape(self) -> Dict:
        shape_map = {"class": "ellipse", "function": "roundrectangle", "module": "diamond", "import": "hexagon"}
        elements = []
        for node in self.nodes:
            elements.append({"data": {"id": node["id"], "label": node["name"], "type": node["type"], "shape": shape_map.get(node["type"], "circle")}})
        for edge in self.edges:
            elements.append({"data": {"id": f"{edge['source']}-{edge['target']}", "source": edge["source"], "target": edge["target"]}})
        return {"elements": elements}

    def get_subgraph(self, center_node_id: str, depth: int = 2) -> Dict:
        visited, subgraph_nodes, subgraph_edges = set(), [], []
        def bfs(node_id: str, current_depth: int):
            if current_depth > depth or node_id in visited:
                return
            visited.add(node_id)
            node = self.get_node(node_id)
            if node:
                subgraph_nodes.append(node)
            for edge in self.adjacency.get(node_id, []):
                if edge not in subgraph_edges:
                    subgraph_edges.append(edge)
                bfs(edge["target"], current_depth + 1)
        bfs(center_node_id, 0)
        return {"nodes": subgraph_nodes, "edges": subgraph_edges}
