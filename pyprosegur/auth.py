"""Authentication and Request Helper."""
import logging

from aiohttp import ClientSession, ClientResponse

LOGGER = logging.getLogger(__name__)

SMART_SERVER_WS = "https://smart.prosegur.com/smart-server/ws"

COUNTRY = {
    "PT": {
        "Origin": "https://smart.prosegur.com/smart-individuo",
        "Referer": "https://smart.prosegur.com/smart-individuo/login.html",
        "origin": "Web",
    },
    "ES": {
        "Origin": "https://alarmas.movistarproseguralarmas.es",
        "Referer": "https://alarmas.movistarproseguralarmas.es/smart-mv/login.html",
        "origin": "WebM",
    },
}


class Auth:
    """Class to make authenticated requests."""

    def __init__(
        self, websession: ClientSession, user: str, password: str, country: str
    ):
        """Initialize the auth."""
        self.websession = websession
        self.user = user
        self.password = password
        self.country = country
        if country not in COUNTRY:
            raise ValueError(f"{country} not in {COUNTRY.keys()}")

        self.smart_token = None

        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": COUNTRY[self.country]["Origin"],
            "Referer": COUNTRY[self.country]["Referer"],
        }

    async def login(self):
        """Login, retrieving Smart Token used for all requests."""
        data = {
            "user": self.user,
            "password": self.password,
            "language": "en_GB",
            "origin": COUNTRY[self.country]["origin"],
            "platform": "smart2",
            "provider": None,
        }

        response = await self.websession.post(
            f"{SMART_SERVER_WS}/access/login",
            json=data,
            headers=self.headers,
        )

        if response.status != 200:
            raise ConnectionRefusedError("Could not login")

        login = await response.json()
        self.headers["X-Smart-Token"] = login["data"]["token"]

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        if self.websession.closed:
            raise ConnectionError("websession with smart.prosegur is closed")

        headers = kwargs.get("headers")

        if headers is None:
            headers = self.headers
        else:
            headers = {**self.headers, **headers}

        if "X-Smart-Token" not in headers:
            LOGGER.debug("No X-Smart-Token, attempting login")
            await self.login()

        resp = await self.websession.request(
            method,
            f"{SMART_SERVER_WS}{path}",
            **kwargs,
            headers=headers,
        )

        if resp.status != 200:
            del self.headers["X-Smart-Token"]
            LOGGER.error(resp.text)
            raise ConnectionError(
                f"{resp.status} couldn't {method} {path}: {resp.text}"
            )

        return resp
