from setuptools import setup, find_packages
import sys

setup(
    name = "awsom",
    version = "0.0.1",
    packages = find_packages(),
    scripts = ['awsom.py'],
    
    # We use boto for interacting with AWS services
    install_requires = ['boto>=2.7.0', 'PyYAML==3.10']    
)
