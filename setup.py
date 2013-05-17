from setuptools import setup, find_packages

setup(
    name = "awsom",
    description = ("Browse your AWS resources using a hierarchical object model"),
    author = "David Losada Carballo",
    author_email = "david@tuxpiper.com",
    version = "0.0.2",
    packages = find_packages(),
    license = 'MIT',
    keywords = "aws internet cloud",
    long_description = open('README.md').read(),
    url = "http://github.com/tuxpiper/awsom",
    zip_safe = True,
    classifiers=[
       "Development Status :: 1 - Planning",
       "Topic :: System",
       "Environment :: Console",
       "Intended Audience :: System Administrators",
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python"
    ],
    
    # We use boto for interacting with AWS services, YAML for storing configuration
    install_requires = ['boto>=2.7.0', 'PyYAML==3.10']    
)
