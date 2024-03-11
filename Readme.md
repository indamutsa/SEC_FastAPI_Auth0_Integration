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

Run the following command to start the server:

```sh
uvicorn application.main:app --reload
```

4. Test the server by visiting the following URLs:

```sh
curl -X 'GET' \
  --url <http://127.0.0.1:8000/api/public>
```

```json
{
  "status": "success",
  "msg": "Hello from a public endpoint! You don't need to be authenticated to see this."
}
```

The private endpoint requires authentication. To test it, run the following command:

```sh
curl -X 'GET' \
  --url '<http://127.0.0.1:8000/api/private>'
    # {"detail": "Not authenticated"}
```

The following should go through since it only needs any header:

```sh
curl -X 'GET' \
  --url '<http://127.0.0.1:8000/api/private>' \\
  --header 'Authorization: Bearer FastAPI is awesome'
```

But this is not right, we should be able to reject requests that do not have a valid token. We will use Auth0 to secure the server.

Set Up an Auth0 API

Before you begin protecting endpoints in your API you’ll need to create an API on the Auth0 Dashboard. If you haven't an Auth0 account, you can sign up for a free one. Then, go to the APIs section and click on Create API.

This will open a new window for configuring the API. Set the following fields in that window:

- Name, a friendly name or description for the API. Enter Fast API Example for this sample.
- Identifier, which is an identifier that the client application uses to request access tokens for the API. Enter the string `https://fastapiexample.com`. This identifier is also known as audience.
- Signing Algorithm, leave the default setting, `RS256`.

After entering those values, click the Create button.

## Configure JSON Web Token (JWT) Validation

The verify method consists of three steps to validate the integrity of the token:

    The code snippet below describes the steps involved in validating a JSON Web Token (JWT):

    1. It retrieves the token from the Authorization header.
    2. The method uses the key ID (kid claim present in the token header) to obtain the key from the JWKS (JSON Web Key Set) for verifying the token signature. If this step encounters any errors, it returns an error message.
    3. Next, the method attempts to decode the JWT using the gathered information. If there are any errors, it returns an error message. If successful, it returns the token payload.

All done! You are ready now to start securing your endpoints.
