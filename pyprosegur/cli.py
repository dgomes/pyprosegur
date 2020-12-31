"""Command Line Interface."""
import pprint
import logging
import aiohttp
import asyncclick as click

from pyprosegur.auth import Auth
from pyprosegur.installation import Installation

logging.basicConfig(level=logging.DEBUG)


@click.group()
@click.argument("username")
@click.argument("password")
@click.pass_context
async def prosegur(ctx, username, password):
    """Set common arguments."""
    ctx.ensure_object(dict)

    ctx.obj["username"] = username
    ctx.obj["password"] = password


@click.command()
@click.pass_context
async def installation(ctx):
    """Get installation status."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password)

        installation = await Installation.retrieve(auth)

        pprint.pprint(installation.data)
        print(installation.status)


@click.command()
@click.pass_context
async def arm(ctx):
    """Arm the Alarm Panel."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password)

        installation = await Installation.retrieve(auth)

        r = await installation.arm(auth)

        print(r)


@click.command()
@click.pass_context
async def disarm(ctx):
    """Disarm the Alarm Panel."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password)

        installation = await Installation.retrieve(auth)

        r = await installation.disarm(auth)

        print(r)

@click.command()
@click.pass_context
async def activity(ctx):
    """Get Alarm Panel Activity."""
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    async with aiohttp.ClientSession() as session:
        auth = Auth(session, username, password)

        installation = await Installation.retrieve(auth)

        r = await installation.activity(auth)

        pprint.pprint(r)



prosegur.add_command(installation)
prosegur.add_command(arm)
prosegur.add_command(disarm)
prosegur.add_command(activity)

if __name__ == "__main__":
    prosegur(obj={})
