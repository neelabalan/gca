from setuptools import setup, find_packages

setup(
    name             = "gca",
    version          = "0.2.0",
    url              = "https://github.com/neelabalan/gca",
    long_description = open('README.md').read(),
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
    entry_points     = {
        "console_scripts": [
            "gca = gca.main:main"
        ]
    },
    setup_requires   = ["wheel"],
)
