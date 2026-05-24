from __future__ import annotations

import random

from auth.models import AccountCard
from auth.protocols import (
    AccountsRepositoryProtocol,
    AuditRepositoryProtocol,
    CodeRepositoryProtocol,
)


class AccountCardService:
    def __init__(
        self,
        accounts: AccountsRepositoryProtocol,
        audit: AuditRepositoryProtocol,
        codes: CodeRepositoryProtocol,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    def create_account(self, email: str):
        account = self.accounts.create_account(email)

        self.audit.log_event(
            account.id,
            "account_created",
            {"email": email},
        )

        return account

    def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        code = str(random.randint(100000, 999999))

        self.codes.set_code(
            account_id,
            code,
            ttl_seconds,
        )

        self.audit.log_event(
            account_id,
            "verification_code_set",
            {"code": code},
        )

    def get_account_card(self, account_id: int):
        account = self.accounts.get_account(account_id)
        has_code = self.codes.has_code(account_id)
        events = self.audit.list_events(account_id)

        return AccountCard(
            account=account,
            has_active_code=has_code,
            events=events,
        )

    def reset(self) -> None:
        self.accounts.clear()
        self.audit.clear()
        self.codes.clear()