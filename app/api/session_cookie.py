


class SessionCookieManager:
    COOKIE_NAME = "session_token"

    def __init__(self,
                 max_age: int = 3600,
                 secure: bool = True,
                 httponly: bool = True,
                 samesite: str = "lax",
                 path: str = "/"):
        self.max_age = max_age
        self.secure = secure
        self.httponly = httponly
        self.samesite = samesite
        self.path = path

    def set_cookie(self, response, jwt_token: str):
        response.set_cookie(
            key=self.COOKIE_NAME,
            value=jwt_token,
            httponly=True,
            secure=False,  # на проде True
            samesite="lax",
            max_age=self.max_age,
            path="/"
        )

    def delete_cookie(self, response):
        response.delete_cookie(self.COOKIE_NAME)

    def get_cookie(self, request) -> str | None:
        return request.cookies.get(self.COOKIE_NAME)
