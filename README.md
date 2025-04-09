# Power of 10

## Introduction

An application which will collect athlete performance results from [thepowerof10.info](https://www.thepowerof10.info/).

## Installation

This project uses uv to manage dependencies. [Set up uv ](https://docs.astral.sh/uv/getting-started/installation/)

```powershell
# Install dependencies
uv sync
```

## Configuration

The app will extract data for athletes defined in the ```config.yml``` file at the root of the repository.

```yaml
athletes:
  1114055: Murray Graham
```
## Running
```powershell
py main.py
```

## Tests
Run tests with optional ```--use-mock``` cli arg.

```powershell
# Use mock thepowerof10.info html responses
py -m pytest -s --use-mock

# Use thepowerof10.info for real responses
py -m pytest -s
```