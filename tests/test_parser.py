"""
CodeGraph-Explorer 测试套件
"""

import unittest
import tempfile
import os
from pathlib import Path
from src.parser import CodeParser, PythonParser
from src.graph_builder import GraphBuilder


class TestPythonParser(unittest.TestCase):
    """Python解析器测试"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_sample.py")
        sample_code = '''"""Sample module."""
import os
class TestClass:
    """Test class."""
    def method_one(self, x):
        return x * 2
def standalone_function(a, b):
    return a + b
'''
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(sample_code)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_file(self):
        parser = PythonParser()
        parser.parse_file(self.test_file)
        self.assertGreater(len(parser.nodes), 0, "应该有解析出的节点")
        module_nodes = [n for n in parser.nodes.values() if n.type == "module"]
        self.assertEqual(len(module_nodes), 1, "应该有一个模块节点")
        class_nodes = [n for n in parser.nodes.values() if n.type == "class"]
        self.assertGreater(len(class_nodes), 0, "应该有类节点")


class TestCodeParser(unittest.TestCase):
    """统一解析器测试"""

    def test_parse_directory(self):
        temp_dir = tempfile.mkdtemp()
        py_file = os.path.join(temp_dir, "sample.py")
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write("def test(): pass\nclass Foo: pass\n")
        try:
            parser = CodeParser()
            result = parser.parse_directory(temp_dir)
            self.assertIn("nodes", result)
            self.assertGreater(len(result["nodes"]), 0)
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestGraphBuilder(unittest.TestCase):
    """图谱构建器测试"""

    def setUp(self):
        self.sample_data = {
            "nodes": [
                {"id": "n1", "name": "Module1", "type": "module", "file_path": "/test.py", "line_start": 1, "line_end": 10},
                {"id": "n2", "name": "Class1", "type": "class", "file_path": "/test.py", "line_start": 5, "line_end": 15},
            ],
            "edges": [
                {"source": "n1", "target": "n2", "relation": "contain"},
            ]
        }

    def test_build_index(self):
        builder = GraphBuilder(self.sample_data)
        self.assertEqual(len(builder.node_by_id), 2)
        self.assertIn("n1", builder.node_by_id)

    def test_get_node(self):
        builder = GraphBuilder(self.sample_data)
        node = builder.get_node("n1")
        self.assertIsNotNone(node)
        self.assertEqual(node["name"], "Module1")

    def test_get_statistics(self):
        builder = GraphBuilder(self.sample_data)
        stats = builder.get_statistics()
        self.assertEqual(stats["total_nodes"], 2)
        self.assertEqual(stats["total_edges"], 1)


if __name__ == '__main__':
    unittest.main()
