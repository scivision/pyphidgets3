#!/usr/bin/env python
req=['nose','Phidgets']
import pip
pip.main(['install'] +req)
# %%
from setuptools import setup

setup(name='pyphidgets',
      packages=['pyphidgets3'],
      description ='cross-platform Python API',
      version = '0.1',
      url = 'https://github.com/scivision/pyphidgets3',
      classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      ],
	  )
