from setuptools import setup, find_packages
import autobrightness

setup(
    name='autobrightness',
    version=autobrightness.__version__,
    python_requires='>=3, <4',
    install_requires=['opencv-python>=4,<4.4.0.42', 'keyboard', 'PyQt5', 'psutil', 'python-xlib'],
    packages=['autobrightness', 'autobrightness.backend', 'autobrightness.gui'],
    include_package_data=True,
    package_data={
        'autobrightness': ['locales/*/LC_MESSAGES/*.mo', 'icon.png']
    },
    entry_points={
    'console_scripts': [
        'autobrightness=autobrightness.__main__:main',
    ],
    }
)