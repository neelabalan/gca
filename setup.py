from setuptools import setup, find_packages

setup(
    name             = "gca",
    version          = "0.1.0",
    url              = "https://github.com/neelabalan/gca",
    long_description = open('README.md').read(),
    author           = "neelabalan",
    author_email     = "neelabalan.n@gmail.com",
    python_requires  = ">=3.7",
    license          = "MIT",
    install_requires = [
        "yaspin>=1.1.0", 
        "requests>=2.20.0",
        "pytablewriter"
    ],
    py_modules       = ['gca'],
    keywords         = "git clone github",
    packages         = find_packages(), 
    entry_points     = {
        "console_scripts": [
            "gca = gca:main"
        ]
    },
    setup_requires   = ["wheel"],
)