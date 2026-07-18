from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol


class NotificationUrgency(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class NotificationMessage:
    notification_id: str
    user_id: str
    subject: str
    body: str
    urgency: NotificationUrgency = NotificationUrgency.NORMAL
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.notification_id.strip() or not self.user_id.strip():
            raise ValueError("notification identity fields must not be empty")
        if not self.subject.strip() or not self.body.strip():
            raise ValueError("notification content must not be empty")


@dataclass(frozen=True, slots=True)
class DeliveryReceipt:
    notification_id: str
    channel_id: str
    accepted: bool
    provider_reference: str | None = None


class NotificationChannel(Protocol):
    channel_id: str

    def deliver(self, message: NotificationMessage) -> DeliveryReceipt: ...
