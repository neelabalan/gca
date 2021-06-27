from setuptools import setup, find_packages
from codecs import open
from inspect import getsource
from os.path import abspath, dirname, join


here = abspath(dirname(getsource(lambda: 0)))

with open(join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name             = "ghub_clone",
    version          = "0.3.0",
    url              = "https://github.com/neelabalan/gca",
    long_description = long_description, 
    long_description_content_type="text/markdown",
    author           = "neelabalan",
    author_email     = "neelabalan.n@gmail.com",
    python_requires  = ">=3.8",
    license          = "MIT",
    install_requires = [
        "requests>=2.20.0",
        "rich>=9.12.3"
    ],
    keywords         = "git clone github",
    packages         = find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]), 
    scripts          =['gca.py'],
    entry_points     = {
        "console_scripts": [ "gca = gca:main" ]
    },
    setup_requires   = ["wheel"],
)
