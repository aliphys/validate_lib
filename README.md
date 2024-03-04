# validate-lib

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/aliphys/validate-lib/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%20|%203.9-blue)](https://www.python.org/downloads/)

A Library for Validation of Arduino Libraries According to Arduino Style Guide.

## Table of Contents
- [validate-lib](#validate-lib)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)

## Installation
To install `validate-lib`, you can use `pip` and access the latest git commit directly:

```shell
pip install git+https://github.com/aliphys/validate-lib.git
```
To access a specific branch, you can instead use:

```shell
pip install git+https://github.com/aliphys/validate-lib.git@[branch]
```

Simple replace `[branch]` with the name of the branch.

## Usage
To use the tool, go to the root directory of the library and run one of the two commands
```shell
validate_lib --general-rules
validate_lib --comment-rules
```

