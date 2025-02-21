"""Installation Representation."""
import enum
import logging
import aiofiles
from aiohttp import ClientConnectionError
from dataclasses import dataclass
from datetime import datetime, timedelta

from pyprosegur.auth import Auth
from pyprosegur.exceptions import BackendError, NotFound

LOGGER = logging.getLogger(__name__)


class Status(enum.Enum):
    """Alarm Panel Status."""

    ALARM = "LE"
    ARMED = "AT"
    DISARMED = "DA"
    ERROR = "error"
    PARTIALLY = "AP"
    POWER_FAILURE = "FC"
    POWER_RESTORED = "RFC"
    IMAGE = "IM"
    ERROR_DISARMED = "EDA"
    ERROR_ARMED_TOTAL = "EAT"
    ERROR_PARTIALLY = "EAP"
    ERROR_ARMED_TOTAL_COMMUNICATIONS = "EAT-COM"
    ERROR_DISARMED_COMMUNICATIONS = "EDA-COM"
    ERROR_PARTIALLY_COMMUNICATIONS = "EAP-COM"
    ERROR_IMAGE_COMMUNCATIONS = "EIM-COM"

    @staticmethod
    def from_str(code):
        """Convert Status Code to Enum."""
        for status in Status:
            if code == str(status.value):
                return status

        raise NotImplementedError(f"'{code}' not an implemented Installation.Status")


@dataclass
class Event:
    """Event in a Prosegur Alarm."""

    ts: datetime
    id: str
    operation: Status
    by: str


@dataclass
class Camera:
    """Prosegur camera."""

    id: str
    description: str


class Installation:
    """Alarm Panel Installation."""

    def __init__(self, contractId):
        """Installation properties."""
        self.data = None
        self.contractId = contractId
        self.installationId = None
        self.cameras = []
        self._status = Status.ERROR

    @classmethod
    async def list(cls, auth: Auth):
        """Retrieve list of constract associated with user."""
        try:
            resp = await auth.request("GET", "/installation")
        except ClientConnectionError as err:
            raise BackendError from err

        resp_json = await resp.json()
        if resp_json["result"]["code"] != 200:
            LOGGER.error(resp_json["result"])
            raise BackendError(resp_json["result"])

        return [
            {"contractId": install["contractId"], "description": install["description"]}
            for install in resp_json["data"]
        ]

    @classmethod
    async def retrieve(cls, auth: Auth, contractId):
        """Retrieve an installation object."""
        self = Installation(contractId)

        try:
            resp = await auth.request("GET", "/installation")
        except ClientConnectionError as err:
            raise BackendError from err

        resp_json = await resp.json()
        if resp_json["result"]["code"] != 200:
            LOGGER.error(resp_json["result"])
            raise BackendError(resp_json["result"])

        for install in resp_json["data"]:
            if install["contractId"] == contractId:
                self.data = install
        if not self.data:
            raise NotFound(f"Contract {contractId} not found")

        self.installationId = self.data["installationId"]

        self._status = Status.from_str(self.data["status"])

        for camera in self.data["detectors"]:
            if camera["type"] == "Camera":
                self.cameras.append(Camera(camera["id"], camera["description"]))

        return self

    @property
    def contract(self):
        """Contract Identifier."""
        return self.contractId

    @property
    def status(self):
        """Alarm Panel Status."""
        return self._status

    async def arm(self, auth: Auth):
        """Order Alarm Panel to Arm itself."""
        if self.status == Status.ARMED:
            return True

        data = {"statusCode": Status.ARMED.value}

        resp = await auth.request(
            "PUT", f"/installation/{self.installationId}/status", json=data
        )

        LOGGER.debug("ARM HTTP status: %s\t%s", resp.status, await resp.text())
        return resp.status == 200

    async def arm_partially(self, auth: Auth):
        """Order Alarm Panel to Arm Partially itself."""
        if self.status == Status.PARTIALLY:
            return True

        data = {"statusCode": Status.PARTIALLY.value}

        resp = await auth.request(
            "PUT", f"/installation/{self.installationId}/status", json=data
        )

        LOGGER.debug("ARM HTTP status: %s\t%s", resp.status, await resp.text())
        return resp.status == 200

    async def disarm(self, auth: Auth):
        """Order Alarm Panel to Disarm itself."""
        if self.status == Status.DISARMED:
            return True

        data = {"statusCode": Status.DISARMED.value}

        resp = await auth.request(
            "PUT", f"/installation/{self.installationId}/status", json=data
        )

        LOGGER.debug("DISARM HTTP status: %s\t%s", resp.status, await resp.text())
        return resp.status == 200

    async def activity(self, auth: Auth, delta=timedelta(hours=24)):
        """Retrieve activity events."""
        date = datetime.now() - delta
        ts = int(date.timestamp()) * 1000
        resp = await auth.request(
            "GET", f"/event/installation/{self.installationId}/less?limitDate?{ts}"
        )

        json = await resp.json()
        LOGGER.debug("Activity: %s", json)

        return json

    async def panel_status(self, auth: Auth):
        """Retrieve Panel Status."""
        resp = await auth.request(
            "GET", f"/installation/{self.installationId}/panel-status"
        )
        json = await resp.json()
        LOGGER.debug("Panel Status: %s", json)
        if "data" in json and "status" in json["data"]:
            self._status = Status.from_str(json["data"]["status"])
        else:
            self._status = Status.ERROR
            LOGGER.error("Installation Panel Status could not be updated: %s", json)

        return json

    async def last_event(self, auth: Auth):
        """Return Last Event."""
        _all = await self.activity(auth)

        def extract_by(description):
            if " by " in description:
                return description.split(" by ")[1]
            return None

        if "data" in _all:
            event = sorted(_all["data"], key=lambda x: x["creationDate"], reverse=True)
            if len(event):
                return Event(
                    ts=datetime.fromtimestamp(event[0]["creationDate"] / 1000),
                    id=event[0]["id"],
                    operation=Status.from_str(event[0]["operation"]),
                    by=extract_by(event[0]["description"]),
                )

        return None

    async def get_image(self, auth: Auth, camera: str, save_to_disk=False):
        """Retrieve image stored in prosegur backend."""
        resp = await auth.request("GET", f"/image/device/{camera}/last")
        if save_to_disk:
            f = await aiofiles.open(f"{camera}.jpg", mode="wb")
            await f.write(await resp.read())
            await f.close()
        else:
            return await resp.read()

    async def request_image(self, auth: Auth, camera: str):
        """Request image update."""
        data = [camera]

        resp = await auth.request(
            "POST", f"/installation/{self.installationId}/images", json=data
        )

        json = await resp.json()
        LOGGER.debug("Request Image %s: %s", camera, json)

        return json
