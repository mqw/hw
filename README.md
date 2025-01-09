# hw

# Test Instructions

## Prerequisites

- Python 3.8+
- python libraries listed in requirements.txt installed in system or virtual python environment
- docker

## Create virtual environment
`python3 -m venv venv`

## Activate virtual environment
`source venv/bin/activate`

## Install Dependencies
`pip install -r requirements.txt`

## Run all tests
`pytest -v`

## Run with XML report
`pytest --junitxml=test-results/results.xml`

## Run specific test
`pytest test_srv.py::test_reverse_positive -v`

## Activate virtual environment
`deactivate`

## Build service image
`docker build -t hw-test .`

## Start service container
`docker run -p 5000:5000 hw-test`

