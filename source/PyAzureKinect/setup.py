from setuptools import setup, find_packages

setup(
    name='k4apybt',
    version='0.1.0',
    author='Jonathan Santos and Reid Sutherland',
    author_email='rssuther@calpoly.edu',
    description='Python interface to K4A Body Tracking interface.',
    keywords='K4A Kinect Azure',
    license='Copyright (C) Microsoft Corporation. All rights reserved.',
    python_requires='>=3.4',
    packages=find_packages(exclude=['docs', 'test*', 'data']),
    extras_require={'dev': ['pytest']},
    tests_require=['pytest'],
    package_data={
        'k4apy': [
                'lib/k4a.dll',
                'lib/depthengine_1_0.dll',
                'lib/k4abttypes.dll',
        ],
    },
    install_requires=[
        'numpy >= 1.15.0',
        
    ],
)