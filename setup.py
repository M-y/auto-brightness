from setuptools import setup, find_packages

with open('autobrightness/VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='autobrightness',
    version=version,
    python_requires='>=3.7, <4',
    install_requires=['opencv-python', 'keyboard'],
    packages=['autobrightness', 'autobrightness.backend'],
    entry_points={
    'console_scripts': [
        'autobrightness=autobrightness:__main__.main',
    ],
    }
)