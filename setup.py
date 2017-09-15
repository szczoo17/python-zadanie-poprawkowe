from setuptools import setup

setup(
    name='skoczekvcs',
    version='1.0',
    description='Version control system',
    url='https://github.com/szczoo17/python-zadanie-poprawkowe',
    entry_points={'console_scripts': ['svcs=skoczekvcs.cli:main']},
    author='Kacper Skoczek',
    packages=['skoczekvcs']
)
