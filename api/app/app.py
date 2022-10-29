from pprint import pprint

from aiohttp import web

from .config import Config
from .database import Database
from .lifespan import startup, shutdown
from .mail import Mail
from .views import signup, verify, login, root, restore


def get_app():
    _app = web.Application()
    _app['config'] = _config = Config()
    _app['mail'] = Mail(_config)
    _app['db'] = Database()
    _app.add_routes([
        web.get("/signup", signup),
        web.get("/restore", restore),
        web.get("/verify", verify),
        web.get("/login", login),
        web.get("/", root)
    ])
    _app.on_startup.append(startup)
    _app.on_shutdown.append(shutdown)
    return _app


def main():
    _app = get_app()
    config = _app['config']
    pprint(config)

    web.run_app(
        app=_app,
        host=config.app.hostname
    )
