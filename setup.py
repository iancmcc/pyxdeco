from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyxdeco',
      version=version,
      description="Extraordinary Decorators",
      long_description=open('README.rst').read(),
      klassifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers"
          "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      keywords='',
      author='Ian McCracken',
      author_email='ian.mccracken@gmail.com',
      url='http://github.com/iancmcc/pyxdeco',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points="""
      """,
      )
