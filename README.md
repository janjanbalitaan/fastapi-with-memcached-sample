# FastAPI with Memcached Implementation

FastAPI with Memcached Implementation Sample using Python 3

Similar implementation with [My Redis Sample](https://github.com/janjanbalitaan/fastapi-with-redis-sample)

## TODOs
* Automated Test Cases

## Requirements
* [Python 3.8.1](https://www.python.org/downloads/release/python-381)
* [Package Manager](https://pip.pypa.io/en/stable/)
* [Memcached](http://www.memcached.org/files/memcached-1.6.17.tar.gz)

## Installation
* Create a virtual environment
```bash
python3 -m venv venv
```
* Enable the virtualenvironment
```bash
source venv/bin/activate
```
* Install libraries
```bash
pip install -r requirements.txt
```
* Create a environment variable file (rename/copy sample.env file to .env and update the values)
```bash
cp sample.env .env
```

## Usage
* Running the application
```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```
## API Documentation
* [Docs](http://localhost:8000/docs) - Swagger Documentation