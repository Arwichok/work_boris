import random
import secrets

from aiohttp import web

from .database import Database
from .mail import Mail
from .utils import get_pin


async def signup(request: web.Request):
    email = request.query.get("email")
    password = request.query.get("password", "")
    db: Database = request.app["db"]
    mail: Mail = request.app["mail"]
    pin: str = get_pin()

    if address := await db.get_address(email):
        if address['verified']:
            return web.json_response(dict(
                error="Address already exist"
            ))
        else:
            pin = address['pin']
    await db.new_address(email, password, pin)
    if await mail.send(
            to=email,
            subject="Your pin",
            content=f"You pin is {pin}"
    ):
        return web.json_response(dict(
            result="Pin send to email"
        ))
    return web.json_response(dict(
            error="Server not connected"
        ))

async def restore(request: web.Request):
    email: str = request.query.get("email")
    db: Database = request.app['db']
    mail: Mail = request.app['mail']
    pin = get_pin()
    if await db.get_address(email):
        await db.restore(email, pin)
        await mail.send(
            to=email,
            subject="Your pin",
            content=f"You pin is {pin}"
        )
        return web.json_response(dict(
            result="Pin send to email"
        ))
    return web.json_response(dict(
        error="Email not found"
    ))


async def verify(request: web.Request):
    email: str = request.query.get("email")
    verified_pin: str = request.query.get("pin")
    db: Database = request.app['db']
    if address := await db.get_address(email):
        if address['pin'] == verified_pin:
            await db.verify(email)
            return web.json_response(dict(
                result="Email verified"
            ))
        return web.json_response(dict(
            error="Wrong pin"
        ))
    return web.json_response(dict(
        error="Email not found"
    ))


async def login(request: web.Request):
    email = request.query.get("email")
    password = request.query.get("password", "")
    db: Database = request.app['db']
    if address := await db.get_address(email):
        if secrets.compare_digest(address['password'], password):
            return web.json_response(dict(
                result="User exist"
            ))
        return web.json_response(dict(
            error="Wrong password"
        ))
    return web.json_response(dict(
        error="Email not found"
    ))


async def root(request: web.Request):
    return web.json_response({
        "user": "Guest"
    })
