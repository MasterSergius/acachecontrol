"""This setup is based on https://blog.ionelmc.ro/2014/05/25/python-packaging/"""

from __future__ import absolute_import

from glob import glob
from os.path import basename, dirname, join, realpath, splitext

from setuptools import find_packages, setup


def read_version():
    """Read version from package init file (__init__.py)"""
    full_path = join(realpath(dirname((__file__))),
                     'src/acachecontrol/__init__.py')
    with open(full_path) as f:
        for line in f:
            if '__version__' in line:
                return line.split('=')[1].strip().strip('"')

# get the dependencies and installs
with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='acachecontrol',
    version=read_version(),
    license='Apache License 2.0',
    description='Cache-Control for aiohttp',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Serhii Buniak, Andrii Ivaniuk',
    author_email='master.sergius@gmail.com, andrii.ivaniuk@gmail.com',
    url='https://github.com/MasterSergius/acachecontrol',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
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
        'Changelog': 'https://github.com/MasterSergius/acachecontrol/blob/master/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/MasterSergius/acachecontrol/issues',
    },
    python_requires='>=3.6,<4.0',
    install_requires=requires,
)
