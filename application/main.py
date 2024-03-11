"""
Python FastAPI Auth0 integration example
"""

from fastapi import FastAPI, Depends # 👈 new imports
from fastapi.security import HTTPBearer # 👈 new imports

# Scheme for authorization header
token_auth_scheme = HTTPBearer() # 👈 new imports

# Create app instance
app = FastAPI()

@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg":("Hello from a public endpoint! You don't need to be "
               "authenticated to see this")
    }

    return result

@app.get("/api/private")
def private(token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""

    result = token.credentials

    return result