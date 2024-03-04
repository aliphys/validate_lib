from setuptools import setup, find_packages
from validate_lib import __version__

setup(
    name='validate_lib',
    version=__version__,

    url='https://github.com/aliphys/validate-lib',
    author='Ali Jahangiri',
    author_email='a.jahangiri@arduino.cc',

    packages=find_packages(),
    
    entry_points={
        'console_scripts': [
            'validate_lib=validate_lib:main',
        ],
    },
    
    install_requires=['regex'], #external packages as dependencies

)