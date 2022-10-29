import logging
from dataclasses import dataclass

import asyncpg

from .config import Config


@dataclass
class Database:
    pool: asyncpg.Pool = None

    async def create_pool(self, config: Config):
        self.pool = await asyncpg.create_pool(
            user=config.db.username,
            host=config.db.hostname,
            password=config.db.password,
            port=config.db.port,
            database=config.db.database
        )
        logging.info("pool created")

    async def create_tables(self):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                CREATE TABLE IF NOT EXISTS addresses (
                    email TEXT PRIMARY KEY,
                    verified BOOL,
                    pin TEXT,
                    password TEXT
                );
            ''')

    async def get_address(self, email: str):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow('''
            SELECT * FROM addresses WHERE email= $1
            ''', email)

    async def new_address(self, email: str, password: str, pin: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('''
                INSERT INTO addresses (
                    email, verified, password, pin
                ) VALUES ($1, $2, $3, $4)
                ''', email, False, password, pin)

    async def verify(self, email: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('''
                UPDATE addresses 
                SET verified = true
                WHERE email = $1
                ''', email)

    async def restore(self, email: str, pin: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('''
                UPDATE addresses 
                SET verified = false, pin = $1
                WHERE email = $2
                ''', pin, email)

