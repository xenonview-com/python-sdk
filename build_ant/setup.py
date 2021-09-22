'''
Created on September 20, 2021

@author: lwoydziak
'''
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='view-python-sdk',
      version='0.0.1',
      maintainer='Luke Woydziak',
      maintainer_email='lwoydziak@gmail.com',
      url='https://github.com/xenonview-com/view-python-sdk',
      download_url='https://github.com/xenonview-com/view-python-sdk/tarball/1.0',
      platforms=["any"],
      description='Python access to Xenon View.',
      long_description=README,
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Natural Language :: English',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Unix Shell',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=[
          'view_python_sdk'
      ],
      install_requires=[
          "singleton3",
          "requests"
      ],
      python_requires='>=3',

      )
