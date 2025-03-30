from src.api.auth.dtos.token import TokenDTO

from src.config.jwt_config import config_token
from src.config.security import settings

from src.apps.auth.exceptions.token import InvalidSignatureError
from src.apps.user.dto import UserDTO

from jwt import ExpiredSignatureError, PyJWTError, decode, encode, get_unverified_header
from datetime import datetime, timedelta


class TokenService:
    def __init__(self) -> None:
        self.access_token_lifetime = config_token.ACCESS_TOKEN_LIFETIME
        self.refresh_token_lifetime = config_token.REFRESH_TOKEN_LIFETIME
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm

    async def create_tokens(self, dto: UserDTO) -> TokenDTO:
        """
        Create both an access token and a refresh token.
        """
        access_token = await self.generate_access_token(dto)
        refresh_token = await self.generate_refresh_token(dto)
        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    def _validate_token(self, token: str) -> str:
        """
        Check the token header to ensure it uses the expected algorithm.
        """
        token_info = get_unverified_header(token)
        if token_info.get("alg") != self.algorithm:
            raise InvalidSignatureError("Key error")
        return token

    async def encode_token(self, payload: dict) -> str:
        """
        Encode a payload into a JWT token.
        Note: PyJWT's encode is synchronous, but we wrap it in an async function
        to match our service's async interface.
        """
        return encode(payload, self.secret_key, algorithm=self.algorithm)

    async def decode_token(self, token: str) -> dict:
        """
        Decode and validate a JWT token.
        """
        try:
            self._validate_token(token)
            return decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token lifetime is expired")
        except PyJWTError:
            raise Exception("Token is invalid")

    async def generate_access_token(self, dto: UserDTO) -> str:
        """
        Generate an access token with a payload that includes user details.
        """
        expire = datetime.now() + timedelta(seconds=self.access_token_lifetime)
        payload = {
            "token_type": "access",
            "user": {"user_id": str(dto.id), "user_name": str(dto.name)},
            "exp": expire,
            "iat": datetime.now(),
        }
        return await self.encode_token(payload)

    async def generate_refresh_token(self, dto: UserDTO) -> str:
        """
        Generate a refresh token. Note that its token_type is set to "refresh".
        """
        expire = datetime.now() + timedelta(seconds=self.refresh_token_lifetime)
        payload = {
            "token_type": "refresh",
            "user": {"user_id": str(dto.id), "user_name": str(dto.name)},
            "exp": expire,
            "iat": datetime.now(),
        }
        return await self.encode_token(payload)
