from distutils.core import setup
from bsg_restapi import __version__

setup(
    name='bsg-restapi',
    version=__version__,
    packages=['bsg_restapi'],
    url='https://github.com/bsgworld/bsg-python',
    license='BSD 2-Clause License',
    author='support@bsg.world',
    author_email='support@bsg.world',
    description='BSG REST API Wrapper'
)
