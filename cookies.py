from requests.cookies import RequestsCookieJar, create_cookie
from linkedin_api.cookie_repository import CookieRepository
import json
import os

# Use cookies from the browser to create a cookie jar
cookies = json.load(open('cookies.json'))  # Path of exported cookie via https://www.editthiscookie.com/

def make_cookie():
    cookie_jar = RequestsCookieJar()
    for cookie_data in cookies['cookies']:
        # print(cookie_data)
        cookie = create_cookie(
            domain=cookie_data["domain"],
            name=cookie_data["name"],
            value=cookie_data["value"],
            path=cookie_data["path"],
            secure=cookie_data["secure"],
            expires=cookie_data.get("expirationDate", None),
            rest={
                "HttpOnly": cookie_data.get("httpOnly", False),
                "SameSite": cookie_data.get("sameSite", "unspecified"),
                "HostOnly": cookie_data.get("hostOnly", False),
            }
        )
        cookie_jar.set_cookie(cookie)

    username = os.getenv("MAIL_F")
    # Save cookies
    new_repo = CookieRepository()
    new_repo.save(cookie_jar, username)

    return cookie_jar

if __name__ == '__main__':
    cook = make_cookie()
    print(cook)
