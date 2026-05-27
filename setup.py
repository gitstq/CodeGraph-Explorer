"""
CodeGraph-Explorer Setup Script
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="codegraph-explorer",
    version="1.0.0",
    author="gitstq",
    description="轻量化代码结构可视化与导航工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/CodeGraph-Explorer",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={"console_scripts": ["codegraph=src.cli:main"]},
)
