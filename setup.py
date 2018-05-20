# Inspired by https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


NAME = 'shyPy'
DESCRIPTION = 'A shy Python package with things I secretly like to use.'
URL = 'https://github.com/grothesk/shyPy'
EMAIL = 'malte.groth@gmx.net'
AUTHOR = 'Malte Groth'
REQUIRES_PYTHON = '>=3.6.0'
REQUIRED = ['pytest']


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name=NAME,
    version='1.0',
    description=DESCRIPTION,
    long_description=readme,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),  # nothing to exclude so far
    install_requires=REQUIRED,
    license=license,
    classifiers=[  # yes, it's planned to have it some day on https://pypi.org
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
