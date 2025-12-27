from app.config import COOKIES_MAX_AGE, COOKIES_SECURE, COOKIES_HTTPONLY, COOKIES_SAME_SITE, COOKIES_PATH
from fastapi import Response

class SessionCookieManager:
    COOKIE_NAME = "session_token"

    def __init__(self):
        self.max_age = COOKIES_MAX_AGE
        self.secure = COOKIES_SECURE
        self.httponly = COOKIES_HTTPONLY
        self.same_site = COOKIES_SAME_SITE
        self.path = COOKIES_PATH

    def set_cookie(self, response: Response, jwt_token: str):
        response.set_cookie(
            key=self.COOKIE_NAME,
            value=jwt_token,
            httponly=self.httponly,
            secure=self.secure,
            samesite=self.same_site,
            max_age=self.max_age,
            path=self.path
        )

    def delete_cookie(self, response):
        response.delete_cookie(self.COOKIE_NAME)

    def get_cookie(self, request) -> str | None:
        return request.cookies.get(self.COOKIE_NAME)
