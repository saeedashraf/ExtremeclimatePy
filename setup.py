from setuptools import setup, find_packages

setup(
    name = 'compound-extremes'
    version = 0.0.1
    author = Saeid A. Vaghefi
    author_email = saeedashrafv@gmail.com
    description = For analyzing compound extreme events
    long_description = file: README.md
    long_description_content_type = text/markdown
    url = https://github.com/saeedashraf/compound-extremes
    classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent
    packages=find_packages(where='src'),
    package_dir={'':'src'},
)