import os
from setuptools import setup, find_packages

with open('version.txt') as f:
    version = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open(os.path.abspath('README.md')) as f:
    readme = f.read()

setup(
    name="rio_gps",
    version=version,
    author="Ruberth Barros",
    author_email="ruberth@protonmail.com",
    description=("Retrieves and stores GPS data from buses of Rio de Janeiro"),
    long_description=readme,
    packages=find_packages(),
    package_data={"": ["*.cfg"]},
    include_package_data=True,
    install_requires=requirements
)
