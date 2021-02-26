# gca (github clone all)
[![codecov](https://codecov.io/gh/neelabalan/gca/branch/main/graph/badge.svg?token=MGFCAJ1UR6)](https://codecov.io/gh/neelabalan/gca)

> simple script to clone all public repositories of a user



## installation

```bash
python3 setup.py install
# git needs to be in system path
```



## usage

```bash
# user
gca --user neelabalan

# to not download github gists of the user
gca --user --ignore-gist neelabalan

# org
gca --user microsoft 
```

