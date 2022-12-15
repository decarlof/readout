from setuptools import setup, find_packages
from setuptools.command.install import install
import os


setup(
    name='readout',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/decarlof/readout',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/readout_cli.py'],  
    entry_points={'console_scripts':['readout = readout_cli:main'],},
    description='cli to measure AreaDetector readout',
    zip_safe=False,
)