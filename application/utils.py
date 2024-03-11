from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from application.config import get_settings
import http.client

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )
# 👇 verify jwt token
class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self):
        self.config = get_settings()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)
        self.config.auth0_issuer = self.config.auth0_issuer + "/"
        print("Expected issuer:", self.config.auth0_issuer)

        # 👇 new code
    async def verify(self,
                     security_scopes: SecurityScopes,
                     token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
                     ):
        if token is None:
            raise UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience,
                issuer=self.config.auth0_issuer,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))
    
        return payload


    # 👆 verify the jwt token
    
    def get_access_token(self):
        settings = get_settings()
        conn = http.client.HTTPSConnection(settings.auth0_domain)


        payload = "{\"client_id\":\"HZ10O5fMXamfBI57ITKCOXhzeuTNXgKK\",\"client_secret\":\"zRsoRyDuY82lIEPcYNsiCgHwjad938QnylNbW53Jm-YD1E9pw21KpkOR7h-SLLhW\",\"audience\":\"https://fastapiexample.com\",\"grant_type\":\"client_credentials\"}"

        headers = { 'content-type': "application/json" }

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

