"""
CodeGraph-Explorer - 轻量化代码结构可视化与导航工具
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .parser import CodeParser
from .graph_builder import GraphBuilder
from .server import create_app

__all__ = ["CodeParser", "GraphBuilder", "create_app"]
