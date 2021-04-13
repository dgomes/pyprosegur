"""Installation Representation."""
import enum
import logging
import datetime

from pyprosegur.auth import Auth

LOGGER = logging.getLogger(__name__)


class Status(enum.Enum):
    """Alarm Panel Status."""

    ARMED = "AT"
    DISARMED = "DA"
    PARTIALLY = "AP"
    ERROR_PARTIALLY = "EAP"

    @staticmethod
    def from_str(code):
        """Convert Status Code to Enum."""
        if code == "AT":
            return Status.ARMED
        if code == "DA":
            return Status.DISARMED
        if code == "AP":
            return Status.PARTIALLY
        if code == "EAP":
            return Status.ERROR_PARTIALLY
        
        raise NotImplementedError(f"'{code}' not an implemented Installation.Status")


class Installation():
    """Alarm Panel Installation."""

    @classmethod
    async def retrieve(cls, auth: Auth, number: int = 0):
        """Retrieve an installation object."""
        self = Installation()
        self.number = number

        resp = await auth.request("GET", "/installation")

        resp_json = await resp.json()
        if resp_json["result"]["code"] != 200:
            LOGGER.error(resp_json["result"])
            return None

        self.data = resp_json["data"][self.number]

        self.installationId = self.data["installationId"]

        return self

    @property
    def contract(self):
        """Contract Identifier."""
        return self.data["contractId"]

    @property
    def status(self):
        """Alarm Panel Status."""
        return Status.from_str(self.data["status"])

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

    async def activity(self, auth: Auth):
        """Retrieve activity events."""
       
        date = datetime.datetime.now() - datetime.timedelta(hours=24)
        ts = int(date.timestamp())*1000
        resp = await auth.request(
            "GET", f"/event/installation/{self.installationId}/less?limitDate?{ts}")

        json = await resp.json()
        LOGGER.debug("Activity: %s", json)

        return json 
