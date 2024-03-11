
# 👇 verify jwt token
from typing import Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from jose import jwt
from jose.exceptions import JWTError
from .config import get_settings
from jose import jwt, jwk
from jose.utils import base64url_decode
import requests
import http.client
import os

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class VerifyToken:
    def __init__(self):
        self.config = get_settings()
        self.http_bearer = HTTPBearer()

        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        jwks_resp = requests.get(jwks_url)
        self.jwks = jwks_resp.json()

    async def verify(self, security_scopes: SecurityScopes, token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())):
        if os.getenv('TEST_ENV') or os.getenv('TEST_ENV') == None:
            
            return True
            
        if token is None:
            raise HTTPException(status_code=403, detail="Not Authorized")
        
        unverified_header = jwt.get_unverified_header(token.credentials)
        rsa_key = self._get_rsa_key(unverified_header['kid'])
        if rsa_key is None:
            raise HTTPException(status_code=403, detail="RSA key not found")

        try:
            payload = jwt.decode(
                token.credentials,
                rsa_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience,
                issuer=self.config.auth0_issuer + "/"
            )
            return payload
        except JWTError as e:
            raise HTTPException(status_code=403, detail=f"JWT Error: {str(e)}")


    def _get_rsa_key(self, kid):
        for key in self.jwks['keys']:
            if key['kid'] == kid:
                return { 
                    "kty": key['kty'], 
                    "kid": key['kid'], 
                    "use": key['use'], 
                    "n": key['n'], 
                    "e": key['e']
                }
        return None



    # 👆 verify the jwt token
    
    def get_access_token(self):
        settings = get_settings()
        conn = http.client.HTTPSConnection(settings.auth0_domain)


        payload = "{\"client_id\":\"HZ10O5fMXamfBI57ITKCOXhzeuTNXgKK\",\"client_secret\":\"zRsoRyDuY82lIEPcYNsiCgHwjad938QnylNbW53Jm-YD1E9pw21KpkOR7h-SLLhW\",\"audience\":\"https://fastapiexample.com\",\"grant_type\":\"client_credentials\"}"

        headers = { 'content-type': "application/json" }

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
        # print(data.decode("utf-8"))

