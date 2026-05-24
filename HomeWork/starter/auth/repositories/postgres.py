from __future__ import annotations

import psycopg
from psycopg.rows import dict_row

from auth.config import Settings
from auth.models import Account


class PostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.conn = psycopg.connect(settings.postgres_dsn)

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL
                )
            """)
            self.conn.commit()

    def create_account(self, email: str):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO accounts(email)
                VALUES (%s)
                RETURNING id, email
                """,
                (email,)
            )

            row = cur.fetchone()
            self.conn.commit()

            return Account(
                id=row["id"],
                email=row["email"]
            )

    def get_account(self, account_id: int):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, email
                FROM accounts
                WHERE id = %s
                """,
                (account_id,)
            )

            row = cur.fetchone()

            if row is None:
                return None

            return Account(
                id=row["id"],
                email=row["email"]
            )

    def clear(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM accounts")
            self.conn.commit()


class AsyncPostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def _get_conn(self):
        return await psycopg.AsyncConnection.connect(
            self.settings.postgres_dsn
        )

    async def create_account(self, email: str):
        conn = await self._get_conn()

        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL
                )
            """)

            await cur.execute(
                """
                INSERT INTO accounts(email)
                VALUES (%s)
                RETURNING id, email
                """,
                (email,)
            )

            row = await cur.fetchone()
            await conn.commit()

        await conn.close()

        return Account(
            id=row["id"],
            email=row["email"]
        )

    async def get_account(self, account_id: int):
        conn = await self._get_conn()

        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT id, email
                FROM accounts
                WHERE id = %s
                """,
                (account_id,)
            )

            row = await cur.fetchone()

        await conn.close()

        if row is None:
            return None

        return Account(
            id=row["id"],
            email=row["email"]
        )

    async def clear(self) -> None:
        conn = await self._get_conn()

        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL
                )
            """)

            await cur.execute("DELETE FROM accounts")
            await conn.commit()

        await conn.close()