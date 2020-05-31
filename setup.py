# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:14:09 2020

@author: Aly
"""

import setuptools

setuptools.setup(
    name = 'target_game',
    version = '4.0',
    author = 'Alisa Balabanova',
    author_email = 'alisa.balabanova@student.uva.nl',
    licence = 'MIT',
    python_requires = '>= 3.7',
    packages = setuptools.find_packages(),
    install_requires = 'psychopy',
    scripts = ['target_game.py'],
)