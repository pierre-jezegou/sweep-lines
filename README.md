
# Sweep Lines Project

## Overview
The Sweep Lines Project is a Python-based application designed to process and visualize geometric data using the sweep line algorithm. The project consists of two main scripts: `sweep_lines.py` and `sweep_lines_to_pgf.py`, along with a `requirements.txt` file that lists the dependencies necessary for running the project.

## Installation
To install the necessary dependencies for the project, run the following command (preferably in a virtual environment):
```sh
pip install -r requirements.txt
```

## Dependencies
The project requires the following Python packages:
- `pylint`: A tool for checking your Python code against coding standards.
- `prettytable`: A simple Python library for displaying tabular data in a visually appealing ASCII table format.
- `jinja2`: A full-featured template engine for Python.
- `sortedcontainers`: A fast, pure-Python implementation of sorted collections.

## Usage

### sweep_lines.py
This script contains the implementation of the sweep line algorithm. To run the script, use the following command:
```sh
python sweep_lines.py
```

### sweep_lines_to_pgf.py
This script processes the output of the sweep line algorithm and generates PGF (Portable Graphics Format) files for visualization. To run the script, use the following command:
```sh
python sweep_lines_to_pgf.py
```

### performances.py
This script contains the implementation of the sweep line algorithm and the brute force algorithm. It compares the performance of the two algorithms on random data sets. To run the script, use the following command:
```sh
python performances.py
```

> [!NOTE]
> You have to redirect the output of the script to a file to save the results. For example:
>    ```sh
>    python performances.py > performances.tex
>    ```

## Project Structure
- `requirements.txt`: Lists all the dependencies required to run the project.
- `sweep_lines.py`: Contains the core implementation of the sweep line algorithm.
- `sweep_lines_to_pgf.py`: Processes the results from `sweep_lines.py` and generates PGF files.
