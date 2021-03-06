[![PyPI](https://img.shields.io/pypi/v/truffleHog3.svg)](https://pypi.org/project/truffleHog3)
![](https://img.shields.io/badge/python-3.6%2B-informational.svg)
[![Build Status](https://travis-ci.com/feeltheajf/truffleHog3.svg?branch=master)](https://travis-ci.com/feeltheajf/truffleHog3)
[![codecov](https://codecov.io/gh/feeltheajf/truffleHog3/branch/master/graph/badge.svg)](https://codecov.io/gh/feeltheajf/truffleHog3)


# truffleHog3
This is an enhanced version of [truffleHog](https://github.com/dxa4481/truffleHog) scanner


## New

- Python 3.6
- flake8 compliant code
- output to file option
- option to disable Git history checks - scan simple files/folders
- option to exclude files/directories


## Installation

Package is available on [PyPI](https://pypi.org/project/truffleHog3)
```
pip install truffleHog3
```


## Customizing

List of regexes was moved into repository, see [regexes.json](https://github.com/feeltheajf/truffleHog3/blob/master/truffleHog3/regexes.json)


## Help

```
usage: trufflehog3 [options] source

Find secrets in your codebase.

positional arguments:
  source              URL or local path for secret searching

optional arguments:
  -h, --help          show this help message and exit
  -r, --rules         ignore default regexes and source from json
  -o, --output        write report to file
  -b, --branch        name of the branch to be scanned
  -m, --max-depth     max commit depth for searching
  -s, --since-commit  scan starting from a given commit hash
  --json              output in JSON
  --exclude           exclude paths from scan
  --no-regex          disable high signal regex checks
  --no-entropy        disable entropy checks
  --no-history        disable commit history check
```


## Thanks

Special thanks to Dylan Ayrey ([@dxa4481](https://github.com/dxa4481)), developer of the original [truffleHog](https://github.com/dxa4481/truffleHog) scanner
