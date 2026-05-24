from __future__ import annotations

import asyncio
import random

from auth.models import AccountCard
from auth.protocols import (
    AsyncAccountsRepositoryProtocol,
    AsyncAuditRepositoryProtocol,
    AsyncCodeRepositoryProtocol,
)


class AsyncAccountCardService:
    def __init__(
        self,
        accounts: AsyncAccountsRepositoryProtocol,
        audit: AsyncAuditRepositoryProtocol,
        codes: AsyncCodeRepositoryProtocol,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    async def create_account(self, email: str):
        account = await self.accounts.create_account(email)

        await self.audit.log_event(
            account.id,
            "account_created",
            {"email": email},
        )

        return account

    async def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        code = str(random.randint(100000, 999999))

        await self.codes.set_code(
            account_id,
            code,
            ttl_seconds,
        )

        await self.audit.log_event(
            account_id,
            "verification_code_set",
            {"code": code},
        )

    async def get_account_card(self, account_id: int):
        account, has_code, events = await asyncio.gather(
            self.accounts.get_account(account_id),
            self.codes.has_code(account_id),
            self.audit.list_events(account_id),
        )

        return AccountCard(
            account=account,
            has_active_code=has_code,
            events=events,
        )

    async def reset(self) -> None:
        await asyncio.gather(
            self.accounts.clear(),
            self.audit.clear(),
            self.codes.clear(),
        )