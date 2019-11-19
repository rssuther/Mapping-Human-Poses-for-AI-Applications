from setuptools import setup, find_packages

setup(
    name='HTTPTransfer',
    version='0.1.0',
    author='Reid Sutherland',
    author_email='rssuther@calpoly.edu',
    description='Python Server Client Interface for Azure Kinect BT.',
    keywords='HTTPTransfer AKC Client Kinect Azure',
    license='Copyright (C) Microsoft Corporation. All rights reserved.',
    python_requires='>=3.4',
    packages=find_packages(exclude=['docs', 'test*', 'data']),
    extras_require={'dev': ['pytest']},
    tests_require=['pytest'],
    install_requires=[
        'numpy >= 1.15.0',
        'pickle',
        
    ],
)