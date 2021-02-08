#NOT WORKING YET
from setuptools import setup, find_packages

MAJOR = 0
MINOR = 9
PATCH = 0
VERSION = "{}.{}.{}".format(MAJOR, MINOR, PATCH)

with open("smda/version.py", "w") as f:
    f.write("__version__ = '{}'\n".format(VERSION))


setup(
    name='smda',
    version=VERSION,
    url='https://github.com/tubiana/SMDAGui_dev',
    license='GPL3',
    author='Thibault Tubiana',
    author_email='tubiana.thibault@gmail.com',
    description='SMDA: Simple Molecular Dynamic Analysis GUI',
    platforms=["Linux", "Solaris", "Mac OS-X", "darwin", "Unix", "win32"],
    install_requires=['matplotlib',
                      'numpy',
                      'pandas',
                      'scipy >= 0.18',
                      'numba',
                      'mdtraj >= 1.9.5',
                      'PyQt5'],

    entry_points={'console_scripts':['smda=smda.smda:main']},


    packages=find_packages(),
)