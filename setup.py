from setuptools import setup, find_packages

setup(
    name='autobrightness',
    version='0.1.0',
    python_requires='>=3.7, <4',
    install_requires=['opencv-python'],
    packages=['autobrightness', 'autobrightness.backend'],
    entry_points={
    'console_scripts': [
        'autobrightness=autobrightness:__main__.main',
    ],
    }
)