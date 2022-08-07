"""Command Line Interface."""
import pprint
import logging
import aiohttp
import asyncclick as click

from pyprosegur.auth import Auth, COUNTRY
from pyprosegur.installation import Installation

logging.basicConfig(level=logging.DEBUG)


@click.group()
@click.argument("username")
@click.argument("password")
@click.argument("country", type=click.Choice(COUNTRY.keys(), case_sensitive=True))
@click.pass_context
async def prosegur(ctx, username, password, country):
    """Set common arguments."""
    ctx.ensure_object(dict)

    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["country"] = country


@click.command()
@click.pass_context
async def installation(ctx):
    """Get installation status."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password, country)

        installation = await Installation.retrieve(auth)

        pprint.pprint(installation.data)
        print(installation.status)


@click.command()
@click.pass_context
async def arm(ctx):
    """Arm the Alarm Panel."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password, country)

        installation = await Installation.retrieve(auth)

        r = await installation.arm(auth)

        print(r)


@click.command()
@click.pass_context
async def disarm(ctx):
    """Disarm the Alarm Panel."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password, country)

        installation = await Installation.retrieve(auth)

        r = await installation.disarm(auth)

        print(r)


@click.command()
@click.pass_context
async def activity(ctx):
    """Get Alarm Panel Activity."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password, country)

        installation = await Installation.retrieve(auth)

        r = await installation.activity(auth)

        pprint.pprint(r)


@click.command()
@click.pass_context
async def last_event(ctx):
    """Get the last event."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password, country)

        installation = await Installation.retrieve(auth)

        r = await installation.last_event(auth)

        pprint.pprint(r)

@click.command()
@click.pass_context
@click.argument("camera")
async def get_image(ctx, camera):
    """Get CAMERA image.

    CAMERA is the Camera ID to get the image from.
    """
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        try:
            auth = Auth(session, username, password, country)

            installation = await Installation.retrieve(auth)

            r = await installation.get_image(auth, camera, save_to_disk=True)

        except ProsegurException as err:
            _LOGGER.error("Image %s doesn't exist: %s", self.camera.description, err)

@click.command()
@click.pass_context
@click.argument("camera")
async def request_image(ctx, camera):
    """Request new CAMERA image.

    CAMERA is the Camera ID to request a new image from.
    """
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    country = ctx.obj["country"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password, country)

        installation = await Installation.retrieve(auth)

        r = await installation.request_image(auth, camera)

        pprint.pprint(r)


prosegur.add_command(installation)
prosegur.add_command(arm)
prosegur.add_command(disarm)
prosegur.add_command(activity)
prosegur.add_command(last_event)
prosegur.add_command(get_image)
prosegur.add_command(request_image)

if __name__ == "__main__":
    prosegur(obj={})
