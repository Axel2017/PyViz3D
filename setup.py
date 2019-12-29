from setuptools import setup

# Read the contents of your README file.
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.1.5'

setup(name='pyviz3d',
      version=version,
      description='PyViz3D is a Python package to visualize 3D point clouds.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/francisengelmann/pyviz3d',
      download_url='https://github.com/francisengelmann/pyviz3d/archive/' + version + '.tar.gz',
      author='Francis Engelmann',
      author_email='francis.engelmann@gmail.com',
      license='MIT',
      packages=['pyviz3d'],
      install_requires=[
          'numpy',
          'vtk',
      ],
      zip_safe=False)
