#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: EyreFree
# Mail: eyrefree@eyrefree.org
# Created Time:  2019-02-05 15:01:34 PM
#############################################


from setuptools import setup, find_packages

setup(
    name = "efpodsanalyzer",
    version = "0.2.3",
    keywords = ("pip", "eyrefree", "cocoapods", "analyzer", "efpodsanalyzer"),
    description = "CocoaPods dependency analysis tool",
    long_description = "CocoaPods dependency analysis tool",
    license = "GPLv3 Licence",

    url = "https://github.com/EyreFree/EFPodsAnalyzer",
    author = "EyreFree",
    author_email = "eyrefree@eyrefree.org",

    packages = find_packages(),
    include_package_data = True,
    package_data={
        'efpodsanalyzer': [
            'EFPADiagram/*.html', 
            'EFPADiagram/js/*',
            'EFPADiagram/css/*', 
            'template/*', 
            'EFPAConfig.json'
        ]
    },
    platforms = "any",
    install_requires = [],
    entry_points={
        'console_scripts':[
            'efpodsanalyzer = efpodsanalyzer.efpodsanalyzer:main'
        ]
    }
)