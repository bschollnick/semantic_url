"""Semantic URL - A Parsing & Manipulation library for creating & using Semantic URLs
"""

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: OS Independent
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
"""
try:
    from setuptools import setup, find_packages
except:
    from disutils.core import setup, find_packages

__title__ = 'Semantic URL'
__version__ = '1.0'
__author__ = 'Benjamin Schollnick'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Benjamin Schollnick'

dependencies = []

doclines = __doc__.split("\n")

#
#   Modelled after requests - https://github.com/kennethreitz/requests/blob/master/setup.py
#
setup(
    name='Semantic URL',
    version='1.0.10',
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    author='Benjamin Schollnick',
    author_email='benjamin@schollnick.net',
    url='https://github.com/bschollnick/Semantic_URL',
    license="MIT",
    maintainer='Benjamin Schollnick',
    maintainer_email='benjamin@schollnick.net',
    packages=find_packages(),
    include_package_data=True,
    download_url = 'https://github.com/bschollnick/Semantic_URL/tarball/1.0',
    install_requires=dependencies,
    keywords = ['semantic', 'URL'],
    classifiers=filter(None, classifiers.split("\n")),
)
