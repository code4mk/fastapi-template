from taskiq import AsyncBroker
from taskiq_redis import (
    RedisStreamBroker,
    RedisStreamClusterBroker,
    RedisStreamSentinelBroker,
    PubSubBroker,
    PubSubSentinelBroker,
    ListQueueBroker,
    ListQueueClusterBroker,
    ListQueueSentinelBroker,
    RedisAsyncResultBackend,
    RedisAsyncClusterResultBackend,
    RedisAsyncSentinelResultBackend,
)

BrokerType = (
    RedisStreamBroker
    | RedisStreamClusterBroker
    | RedisStreamSentinelBroker
    | PubSubBroker
    | PubSubSentinelBroker
    | ListQueueBroker
    | ListQueueClusterBroker
    | ListQueueSentinelBroker
)

BackendType = (
    RedisAsyncResultBackend | RedisAsyncClusterResultBackend | RedisAsyncSentinelResultBackend
)


def _create_result_backend(
    backend_type: str,
    url: str,
    cluster_hosts: list[str] | None,
    sentinel_hosts: list[str] | None,
    sentinel_service: str | None,
) -> BackendType:
    """Create and return the appropriate result backend."""
    if backend_type == "redis":
        return RedisAsyncResultBackend(url)
    if backend_type == "redis-cluster":
        if not cluster_hosts:
            msg = "cluster_hosts required for redis-cluster backend"
            raise ValueError(msg)
        return RedisAsyncClusterResultBackend(cluster_hosts)
    if backend_type == "redis-sentinel":
        if not sentinel_hosts or not sentinel_service:
            msg = "sentinel_hosts & sentinel_service required"
            raise ValueError(msg)
        parsed = [tuple(h.split(":")) for h in sentinel_hosts]
        return RedisAsyncSentinelResultBackend(parsed, sentinel_service)

    msg = f"Unsupported backend_type: {backend_type}"
    raise ValueError(msg)


def _create_stream_broker(
    broker_type: str,
    url: str,
    cluster_hosts: list[str] | None,
    sentinel_hosts: list[str] | None,
    sentinel_service: str | None,
) -> BrokerType | None:
    """Create Redis stream brokers."""
    if broker_type == "redis-stream":
        return RedisStreamBroker(url)
    if broker_type == "redis-stream-cluster":
        if not cluster_hosts:
            msg = "cluster_hosts required for redis-stream-cluster"
            raise ValueError(msg)
        return RedisStreamClusterBroker(cluster_hosts)
    if broker_type == "redis-stream-sentinel":
        if not sentinel_hosts or not sentinel_service:
            msg = "sentinel_hosts & sentinel_service required"
            raise ValueError(msg)
        parsed = [tuple(h.split(":")) for h in sentinel_hosts]
        return RedisStreamSentinelBroker(parsed, sentinel_service)
    return None


def _create_pubsub_broker(
    broker_type: str,
    url: str,
    sentinel_hosts: list[str] | None,
    sentinel_service: str | None,
) -> BrokerType | None:
    """Create PubSub brokers."""
    if broker_type == "pubsub":
        return PubSubBroker(url)
    if broker_type == "pubsub-sentinel":
        if not sentinel_hosts or not sentinel_service:
            msg = "sentinel_hosts & sentinel_service required"
            raise ValueError(msg)
        parsed = [tuple(h.split(":")) for h in sentinel_hosts]
        return PubSubSentinelBroker(parsed, sentinel_service)
    return None


def _create_list_broker(broker_type: str) -> BrokerType | None:
    """Create List queue brokers."""
    if broker_type == "list":
        return ListQueueBroker()
    if broker_type == "list-cluster":
        return ListQueueClusterBroker()
    if broker_type == "list-sentinel":
        return ListQueueSentinelBroker()
    return None


def _create_broker_instance(
    broker_type: str,
    url: str,
    cluster_hosts: list[str] | None,
    sentinel_hosts: list[str] | None,
    sentinel_service: str | None,
) -> BrokerType:
    """Create and return the appropriate broker instance."""
    # Try stream brokers
    broker = _create_stream_broker(
        broker_type, url, cluster_hosts, sentinel_hosts, sentinel_service
    )
    if broker:
        return broker

    # Try pubsub brokers
    broker = _create_pubsub_broker(broker_type, url, sentinel_hosts, sentinel_service)
    if broker:
        return broker

    # Try list brokers
    broker = _create_list_broker(broker_type)
    if broker:
        return broker

    msg = f"Unsupported broker_type: {broker_type}"
    raise ValueError(msg)


def create_broker(
    broker_type: str = "redis-stream",
    backend_type: str = "redis",
    url: str = "redis://localhost:6379/0",
    sentinel_hosts: list[str] | None = None,
    sentinel_service: str | None = None,
    cluster_hosts: list[str] | None = None,
) -> AsyncBroker:
    """
    Create a Taskiq broker and attach its result backend in one call.

    Returns:
        broker (Taskiq Broker instance with .with_result_backend attached)

    """
    # Create result backend
    backend = _create_result_backend(
        backend_type, url, cluster_hosts, sentinel_hosts, sentinel_service
    )

    # Create broker instance
    broker = _create_broker_instance(
        broker_type, url, cluster_hosts, sentinel_hosts, sentinel_service
    )

    # Attach backend and return
    return broker.with_result_backend(backend)
