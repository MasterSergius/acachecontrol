from __future__ import absolute_import

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import realpath
from os.path import splitext

from read_version import read_version
from setuptools import find_packages
from setuptools import setup

package_path = join(realpath(dirname((__file__))), 'src/acachecontrol')

setup(
    name='acachecontrol',
    version=read_version(package_path, '__init__.py'),
    license='Apache License 2.0',
    description='Cache-Control for aiohttp',
    author='Serhii Buniak',
    author_email='master.sergius@gmail.com',
    url='https://github.com/MasterSergius/acachecontrol',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Changelog': 'https://github.com/MasterSerius/async_cache_control/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/MasterSergius/async_cache_control/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp',
        'CacheControl',
        'py-memoize',
    ]
)
