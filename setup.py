from setuptools import setup, find_packages

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='autobrightness',
    version=version,
    python_requires='>=3.7, <4',
    install_requires=['opencv-python', 'keyboard', 'PyQt5'],
    packages=['autobrightness', 'autobrightness.backend'],
    include_package_data=True,
    package_data={'autobrightness': ['locales/*/LC_MESSAGES/*.mo']},
    entry_points={
    'console_scripts': [
        'autobrightness=autobrightness:__main__.main',
    ],
    }
)