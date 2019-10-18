__version__ = '0.0.1'

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)

with open(os.path.join(here, 'README.md')) as readme_file:
    readme = readme_file.read()

setup_args = dict(
    name='amundsenatlastypes',
    version=__version__,
    description=('Custom Amundsen Atlas data types definition'),
    long_description=readme,
    author="Damian Warszawski",
    maintainer="Verdan Mahmood",
    maintainer_email='verdan.mahmood@gmail.com',
    url='https://github.com/dwarszawski/amundsen-atlas-types',
    packages=find_packages(include=['amundsenatlastypes']),
    include_package_data=True,
    install_requires=[
        'pyatlasclient',
    ],
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='apache atlas, atlas types, amundsen, amundsen atlas',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)

setup(**setup_args)
