# Build and Secure a FastAPI Server with Auth0

This is a simple example of how to build and secure a FastAPI server with Auth0.

## Prerequisites

- Python 3.8 or later
- Auth0 account

## Getting Started

1. Create pythion virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install fastapi 'uvicorn[standard]' pydantic-settings 'pyjwt[crypto]'
pip freeze > requirements.txt
```

2. Create `main.py` file by running the following command in the terminal:

```sh
code main.py
```

3. Add some code in the main.py file. Both a private and public endpoint are created.
