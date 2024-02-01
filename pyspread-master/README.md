# pyspread

[![pypi version](https://img.shields.io/pypi/v/pyspread.svg)](https://pypi.python.org/pypi/pyspread)
[![CI pipeline](https://gitlab.com/pyspread/pyspread/badges/master/pipeline.svg)](https://gitlab.com/pyspread/pyspread/-/pipelines?page=1&scope=branches&ref=master)
[![pyspread community board](https://badges.gitter.im/pyspread/community.svg)](https://gitter.im/pyspread/community)

**pyspread** is a non-traditional spreadsheet that is
based on and written in the programming language Python.

It is released under the [GPL v3. LICENSE](LICENSE)

- Homepage: https://pyspread.gitlab.io/
- Repository: https://gitlab.com/pyspread/pyspread
- API Docs: https://pyspread.gitlab.io/pyspread/


# Installation

The table below shows for which operating systems, pyspread is available in which version.
If pyspread is unavailable or outdated for your operating system, you can install it using one of the three methods below.

![Packaged](https://repology.org/badge/vertical-allrepos/pyspread.svg?header&columns=4)

### With pip

```bash
pip install pyspread
```

### From git

It is assumed that python3 and git are installed.

**Get sources and enter dir**
```bash
git clone https://gitlab.com/pyspread/pyspread.git
# or
git clone git@gitlab.com:pyspread/pyspread.git
# then
cd pyspread
```

**Install dependencies and pyspread**
```bash
pip3 install -r requirements.txt
# or if pip3 is not present
pip install -r requirements.txt
# next
python3 setup.py install
```

## Getting the bleeding edge version from the code repository

Note that there may unfixed bugs if you use the latest repository version.
You may want to check the CI, which comprises unit tests at
`https://gitlab.com/pyspread/pyspread/pipelines`.

Get the latest tarball or zip at https://gitlab.com/pyspread/pyspread or
clone the git repo at `https://gitlab.com/pyspread/pyspread.git`

# Starting pyspread

With an installation via pip, distutils or your OS's installer, simply run
```
$ pyspread
```
from any directory.

In order to start pyspread without installation directly from the cloned
repository or the extracted tarball or zip, run
```
$ ./pyspread/pyspread.py
```
or
```
$ python -m pyspread
```
inside the top directory.

# Contribute

## Issues

Please submit issues in the gitlab issue tracker at
- https://gitlab.com/pyspread/pyspread/issues

## Code

Commit your changes, push them into your fork and send a pull request.

This page gives an overview how to do this:
- https://help.github.com/articles/fork-a-repo

You can find more more details about code organization at
- https://pyspread.gitlab.io/pyspread/