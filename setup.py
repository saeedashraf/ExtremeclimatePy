from setuptools import setup, find_packages

setup(
    name = 'compound-extremes',
    version = '0.0.1',
    author = 'Saeid A. Vaghefi',
    author_email = 'saeedashrafv@gmail.com',
    url = 'https://github.com/saeedashraf/compound-extremes',
    classifiers = 'Programming Language :: Python :: 3  License :: OSI Approved :: MIT License  Operating System :: OS Independent',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
)