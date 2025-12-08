"""Redis-backed schedule source for TaskIQ scheduler."""

import json
from typing import Any

import redis.asyncio as redis
from taskiq.abc.schedule_source import ScheduleSource
from taskiq.scheduler.scheduled_task import ScheduledTask


class RedisScheduleSource(ScheduleSource):
    """Schedule source that uses Redis for persistent storage across processes."""

    def __init__(
        self, redis_url: str = "redis://localhost:6379/0", key_prefix: str = "taskiq:schedules"
    ) -> None:
        """
        Initialize the Redis schedule source.

        Args:
            redis_url: Redis connection URL
            key_prefix: Prefix for Redis keys

        """
        self.redis_url = redis_url
        self.key_prefix = key_prefix
        self._redis: redis.Redis | None = None

    async def _get_redis(self) -> redis.Redis:
        """Get Redis connection, creating it if needed."""
        if self._redis is None:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
        return self._redis

    def _get_schedule_key(self, schedule_id: str) -> str:
        """Get Redis key for a schedule."""
        return f"{self.key_prefix}:{schedule_id}"

    def _get_list_key(self) -> str:
        """Get Redis key for the schedule list."""
        return f"{self.key_prefix}:list"

    async def get_schedules(self) -> list[ScheduledTask]:
        """Get list of all scheduled tasks from Redis."""
        redis_client = await self._get_redis()

        # Get all schedule IDs
        schedule_ids = await redis_client.smembers(self._get_list_key())

        schedules = []
        for schedule_id in schedule_ids:
            schedule_data = await redis_client.hgetall(self._get_schedule_key(schedule_id))
            if schedule_data:
                # Reconstruct ScheduledTask from stored data
                schedule = self._deserialize_schedule(schedule_data)
                if schedule:
                    schedules.append(schedule)

        return schedules

    async def add_schedule(self, schedule: ScheduledTask) -> None:
        """
        Add a new schedule to Redis.

        Args:
            schedule: The ScheduledTask to add

        """
        redis_client = await self._get_redis()

        # Serialize the schedule
        schedule_data = self._serialize_schedule(schedule)

        # Store in Redis
        await redis_client.hset(self._get_schedule_key(schedule.schedule_id), mapping=schedule_data)

        # Add to the list of schedule IDs
        await redis_client.sadd(self._get_list_key(), schedule.schedule_id)

    async def delete_schedule(self, schedule_id: str) -> None:
        """
        Delete a schedule by its ID from Redis.

        Args:
            schedule_id: The ID of the schedule to delete

        Raises:
            KeyError: If the schedule ID is not found

        """
        redis_client = await self._get_redis()

        # Check if schedule exists
        exists = await redis_client.exists(self._get_schedule_key(schedule_id))
        if not exists:
            msg = f"Schedule with ID '{schedule_id}' not found"
            raise KeyError(msg)

        # Delete the schedule data
        await redis_client.delete(self._get_schedule_key(schedule_id))

        # Remove from the list of schedule IDs
        await redis_client.srem(self._get_list_key(), schedule_id)

    async def get_schedule_by_id(self, schedule_id: str) -> ScheduledTask | None:
        """
        Get a schedule by its ID from Redis.

        Args:
            schedule_id: The ID of the schedule to retrieve

        Returns:
            The ScheduledTask if found, None otherwise

        """
        redis_client = await self._get_redis()

        schedule_data = await redis_client.hgetall(self._get_schedule_key(schedule_id))
        if not schedule_data:
            return None

        return self._deserialize_schedule(schedule_data)

    async def list_schedule_ids(self) -> list[str]:
        """
        Get list of all schedule IDs from Redis.

        Returns:
            List of schedule IDs

        """
        redis_client = await self._get_redis()
        schedule_ids = await redis_client.smembers(self._get_list_key())
        return list(schedule_ids)

    async def clear_all_schedules(self) -> int:
        """
        Clear all schedules from Redis.

        Returns:
            Number of schedules that were cleared

        """
        redis_client = await self._get_redis()

        # Get all schedule IDs
        schedule_ids = await redis_client.smembers(self._get_list_key())
        count = len(schedule_ids)

        if count > 0:
            # Delete all schedule data
            keys_to_delete = [self._get_schedule_key(sid) for sid in schedule_ids]
            keys_to_delete.append(self._get_list_key())
            await redis_client.delete(*keys_to_delete)

        return count

    def get_schedule_count(self) -> int:
        """
        Get the number of schedules (synchronous method for compatibility).

        Note: This is a synchronous method that won't work with Redis.
        Use async methods instead.

        Returns:
            Number of schedules

        """
        # This method can't be async but Redis operations are async
        # We'll need to handle this differently
        return 0

    async def get_schedule_count_async(self) -> int:
        """
        Get the number of schedules from Redis (async version).

        Returns:
            Number of schedules

        """
        redis_client = await self._get_redis()
        return await redis_client.scard(self._get_list_key())

    def _serialize_schedule(self, schedule: ScheduledTask) -> dict[str, str]:
        """Serialize a ScheduledTask to Redis-compatible format."""
        return {
            "task_name": schedule.task_name,
            "schedule_id": schedule.schedule_id,
            "cron": schedule.cron or "",
            "labels": json.dumps(schedule.labels or {}),
            "args": json.dumps(schedule.args or []),
            "kwargs": json.dumps(schedule.kwargs or {}),
            "task_id": schedule.task_id or "",
            "time": schedule.time.isoformat() if schedule.time else "",
            "interval": str(schedule.interval) if schedule.interval else "",
        }

    def _deserialize_schedule(self, data: dict[str, Any]) -> ScheduledTask | None:
        """Deserialize Redis data back to ScheduledTask."""
        try:
            # Parse JSON fields
            labels = json.loads(data.get("labels", "{}"))
            args = json.loads(data.get("args", "[]"))
            kwargs = json.loads(data.get("kwargs", "{}"))

            # Create ScheduledTask
            return ScheduledTask(
                task_name=data["task_name"],
                schedule_id=data["schedule_id"],
                cron=data.get("cron") or None,
                labels=labels,
                args=args,
                kwargs=kwargs,
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error deserializing schedule: {e}")  # noqa: T201
            return None

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.aclose()
