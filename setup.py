import imp
import sys
from distutils.core import setup

ignis = imp.load_source("", "scripts/ignis")

mainscript = "scripts/ignis"

if sys.version_info < (3, 0, 0):
    print(mainscript + " requires Python 3")

setup(
    name="ignis",
    description="Console-based website building program",
    author=ignis.AUTHOR,
    author_email="development@pariahvi.com",
    license="BSD",
    version=ignis.VERSION,
    url="https://github.com/PariahVi/ignis",
    scripts=[mainscript],
    platforms="No particular restrictions",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Operating System :: OS Independent",
        "Topic :: Other/Nonlisted Topic"
    ]
)
