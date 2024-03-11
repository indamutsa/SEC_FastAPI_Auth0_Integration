import jwt
from fastapi import HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from application.config import get_settings

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Retuns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )
# 👇 verify jwt token
class VerifyToken:
    """Does all the token verification using"""

    def __init__(self) -> None:
        self.config = get_settings()

        # This get the JWKs from a given URL and does not processing so you can
        # Use any of the keys available

        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)
# 👆 verify the jwt token