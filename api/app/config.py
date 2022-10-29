import os
from dataclasses import dataclass, field


@dataclass
class Mail:
    hostname: str = os.getenv("MAIL_HOSTNAME")
    password: str = os.getenv("MAIL_PASSWORD")
    username: str = os.getenv("MAIL_USERNAME")
    port: int = int(os.getenv("MAIL_PORT", 465))


@dataclass
class App:
    hostname: str = os.getenv("APP_HOSTNAME")


@dataclass
class DB:
    username: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
    hostname: str = os.getenv("POSTGRES_HOSTNAME")
    database: str = os.getenv("POSTGRES_DB")
    port: int = int(os.getenv("POSTGRES_PORT", 5432))


@dataclass
class Config:
    mail: Mail = field(default_factory=Mail)
    app: App = field(default_factory=App)
    db: DB = field(default_factory=DB)
