from .config import Config
from .database import Database
from .mail import Mail


async def startup(app):
    config: Config = app['config']
    mail: Mail = app['mail']
    db: Database = app['db']
    await db.create_pool(config)
    await db.create_tables()
    await mail.connect()
    await mail.smtp.login(
        username=config.mail.username,
        password=config.mail.password
    )


async def shutdown(app):
    db: Database = app['db']
    await db.pool.close()
