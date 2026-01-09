"""Events module - Azure Event Hub integration and event streaming."""

from .publisher import publish_event, EventPublisher

__all__ = ["publish_event", "EventPublisher"]
