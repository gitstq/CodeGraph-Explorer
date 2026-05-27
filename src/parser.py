"""
代码解析器模块 - 支持多种编程语言的AST解析
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class CodeNode:
    """代码节点"""
    id: str
    name: str
    type: str
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    parameters: Optional[List[str]] = None
    children: Optional[List[str]] = None


@dataclass
class CodeEdge:
    """代码关系边"""
    source: str
    target: str
    relation: str


class PythonParser:
    """Python代码解析器"""

    def __init__(self):
        self.nodes: Dict[str, CodeNode] = {}
        self.edges: List[CodeEdge] = []
        self.node_counter = 0

    def _generate_node_id(self, name: str, node_type: str) -> str:
        self.node_counter += 1
        return f"{node_type}_{name}_{self.node_counter}"

    def _get_docstring(self, node: ast.AST) -> Optional[str]:
        docstring = ast.get_docstring(node)
        if docstring and len(docstring) > 200:
            return docstring[:200] + "..."
        return docstring

    def _get_parameters(self, node) -> List[str]:
        return [arg.arg for arg in node.args.args]

    def parse_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content, filename=file_path)

            module_id = self._generate_node_id(os.path.basename(file_path), "module")
            module_node = CodeNode(
                id=module_id,
                name=os.path.basename(file_path),
                type="module",
                file_path=file_path,
                line_start=1,
                line_end=len(content.split('\n'))
            )
            self.nodes[module_id] = module_node

            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    self._process_definition(node, module_id)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        import_id = self._generate_node_id(alias.name, "import")
                        import_node = CodeNode(
                            id=import_id, name=alias.name, type="import",
                            file_path=file_path, line_start=node.lineno, line_end=node.lineno
                        )
                        self.nodes[import_id] = import_node
                        self.edges.append(CodeEdge(module_id, import_id, "import"))
                elif isinstance(node, ast.ImportFrom) and node.module:
                    import_id = self._generate_node_id(node.module, "import")
                    if import_id not in self.nodes:
                        import_node = CodeNode(
                            id=import_id, name=node.module, type="import",
                            file_path=file_path, line_start=node.lineno, line_end=node.lineno
                        )
                        self.nodes[import_id] = import_node
                        self.edges.append(CodeEdge(module_id, import_id, "import"))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    def _process_definition(self, node, parent_id: str) -> None:
        node_type = "class" if isinstance(node, ast.ClassDef) else "function"
        if isinstance(node, ast.AsyncFunctionDef):
            node_type = "function"
        node_id = self._generate_node_id(node.name, node_type)
        params = self._get_parameters(node) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else None
        code_node = CodeNode(
            id=node_id, name=node.name, type=node_type,
            file_path=file_path if hasattr(self, 'file_path') else node.name,
            line_start=node.lineno, line_end=node.end_lineno or node.lineno,
            docstring=self._get_docstring(node), parameters=params
        )
        self.nodes[node_id] = code_node
        self.edges.append(CodeEdge(parent_id, node_id, "contain"))
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self._process_definition(item, node_id)


class JavaScriptParser:
    """JavaScript代码解析器（简化版）"""

    def __init__(self):
        self.nodes: Dict[str, CodeNode] = {}
        self.edges: List[CodeEdge] = []
        self.node_counter = 0

    def _generate_node_id(self, name: str, node_type: str) -> str:
        self.node_counter += 1
        return f"{node_type}_{name}_{self.node_counter}"

    def parse_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            module_id = self._generate_node_id(os.path.basename(file_path), "module")
            module_node = CodeNode(
                id=module_id, name=os.path.basename(file_path), type="module",
                file_path=file_path, line_start=1, line_end=len(content.split('\n'))
            )
            self.nodes[module_id] = module_node

            patterns = [
                (r'import\s+(?:{\s*)?(\w+)', 'import'),
                (r'import\s+(\w+)\s+from', 'import'),
                (r'function\s+(\w+)\s*\(', 'function'),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(', 'function'),
                (r'class\s+(\w+)', 'class'),
            ]

            for i, line in enumerate(content.split('\n'), 1):
                for pattern, node_type in patterns:
                    match = re.search(pattern, line)
                    if match:
                        name = match.group(1)
                        node_id = self._generate_node_id(name, node_type)
                        if node_id not in self.nodes:
                            node = CodeNode(
                                id=node_id, name=name, type=node_type,
                                file_path=file_path, line_start=i, line_end=i
                            )
                            self.nodes[node_id] = node
                            self.edges.append(CodeEdge(module_id, node_id, "contain" if node_type != "import" else "import"))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")


class CodeParser:
    """统一代码解析器"""

    SUPPORTED_EXTENSIONS = {'.py': PythonParser, '.js': JavaScriptParser, '.jsx': JavaScriptParser, '.ts': JavaScriptParser, '.tsx': JavaScriptParser}

    def __init__(self):
        self.all_nodes: Dict[str, CodeNode] = {}
        self.all_edges: List[CodeEdge] = []

    def parse_directory(self, directory: str) -> Dict:
        path = Path(directory)
        for ext, parser_class in self.SUPPORTED_EXTENSIONS.items():
            for file_path in path.rglob(f"*{ext}"):
                if self._should_ignore(file_path):
                    continue
                parser = parser_class()
                parser.parse_file(str(file_path))
                for node_id, node in parser.nodes.items():
                    self.all_nodes[node_id] = node
                self.all_edges.extend(parser.edges)
        return self.to_dict()

    def parse_file(self, file_path: str) -> Dict:
        path = Path(file_path)
        ext = path.suffix
        if ext in self.SUPPORTED_EXTENSIONS:
            parser_class = self.SUPPORTED_EXTENSIONS[ext]
            parser = parser_class()
            parser.parse_file(file_path)
            for node_id, node in parser.nodes.items():
                self.all_nodes[node_id] = node
            self.all_edges.extend(parser.edges)
        return self.to_dict()

    def _should_ignore(self, path: Path) -> bool:
        ignore_dirs = {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build'}
        for part in path.parts:
            if part in ignore_dirs:
                return True
        return False

    def to_dict(self) -> Dict:
        return {"nodes": [asdict(node) for node in self.all_nodes.values()], "edges": [asdict(edge) for edge in self.all_edges]}
