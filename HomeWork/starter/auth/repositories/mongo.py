from __future__ import annotations

from datetime import datetime

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from auth.config import Settings
from auth.models import AuditEvent


class MongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.client = MongoClient(settings.mongo_dsn)
        self.db = self.client[settings.mongo_db_name]
        self.collection = self.db.audit

    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        self.collection.insert_one({
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload,
            "created_at": datetime.utcnow(),
        })

    def list_events(self, account_id: int, limit: int = 5):
        docs = self.collection.find(
            {"account_id": account_id}
        ).sort("created_at", -1).limit(limit)

        result = []

        for doc in docs:
            result.append(
                AuditEvent(
                    account_id=doc["account_id"],
                    event_type=doc["event_type"],
                    payload=doc["payload"],
                    created_at=doc["created_at"],
                )
            )

        return result

    def clear(self) -> None:
        self.collection.delete_many({})


class AsyncMongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.client = AsyncIOMotorClient(settings.mongo_dsn)
        self.db = self.client[settings.mongo_db_name]
        self.collection = self.db.audit

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        await self.collection.insert_one({
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload,
            "created_at": datetime.utcnow(),
        })

    async def list_events(self, account_id: int, limit: int = 5):
        cursor = self.collection.find(
            {"account_id": account_id}
        ).sort("created_at", -1).limit(limit)

        result = []

        async for doc in cursor:
            result.append(
                AuditEvent(
                    account_id=doc["account_id"],
                    event_type=doc["event_type"],
                    payload=doc["payload"],
                    created_at=doc["created_at"],
                )
            )

        return result

    async def clear(self) -> None:
        await self.collection.delete_many({})