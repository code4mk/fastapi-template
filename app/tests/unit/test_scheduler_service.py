import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime, timedelta

from taskiq.scheduler.scheduled_task import ScheduledTask

from app.services.scheduler_service import SchedulerService


def _make_task(**overrides) -> ScheduledTask:
    defaults = {
        "task_name": "test_task",
        "labels": {"task-type": "schedule"},
        "args": [],
        "kwargs": {},
        "schedule_id": "sched-001",
        "cron": "*/5 * * * *",
    }
    defaults.update(overrides)
    return ScheduledTask(**defaults)


@pytest.fixture
def mock_dynamic_source():
    source = AsyncMock()
    return source


@pytest.fixture
def scheduler_service(mock_dynamic_source):
    with (
        patch("app.services.scheduler_service.get_taskiq_scheduler"),
        patch("app.services.scheduler_service.get_dynamic_schedule_source", return_value=mock_dynamic_source),
    ):
        service = SchedulerService()
    return service


# ── add_scheduled_task ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_add_scheduled_task_success(scheduler_service, mock_dynamic_source):
    task = _make_task()
    mock_dynamic_source.add_schedule.return_value = None

    result = await scheduler_service.add_scheduled_task(task)

    assert result["success"] is True
    assert "registered successfully" in result["message"]
    assert result["task_info"]["task_name"] == "test_task"
    assert result["task_info"]["schedule_id"] == "sched-001"
    assert result["task_info"]["cron"] == "*/5 * * * *"
    mock_dynamic_source.add_schedule.assert_awaited_once_with(task)


@pytest.mark.asyncio
async def test_add_scheduled_task_value_error(scheduler_service, mock_dynamic_source):
    task = _make_task()
    mock_dynamic_source.add_schedule.side_effect = ValueError("bad value")

    result = await scheduler_service.add_scheduled_task(task)

    assert result["success"] is False
    assert "Failed to register" in result["message"]
    assert result["task_info"] is None


@pytest.mark.asyncio
async def test_add_scheduled_task_runtime_error(scheduler_service, mock_dynamic_source):
    task = _make_task()
    mock_dynamic_source.add_schedule.side_effect = RuntimeError("connection lost")

    result = await scheduler_service.add_scheduled_task(task)

    assert result["success"] is False
    assert "connection lost" in result["message"]


# ── remove_scheduled_task ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_remove_scheduled_task_success(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.delete_schedule.return_value = None

    result = await scheduler_service.remove_scheduled_task("sched-001")

    assert result["success"] is True
    assert "removed successfully" in result["message"]
    mock_dynamic_source.delete_schedule.assert_awaited_once_with("sched-001")


@pytest.mark.asyncio
async def test_remove_scheduled_task_not_found(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.delete_schedule.side_effect = KeyError("not found")

    result = await scheduler_service.remove_scheduled_task("missing-id")

    assert result["success"] is False
    assert "not found" in result["message"]


@pytest.mark.asyncio
async def test_remove_scheduled_task_runtime_error(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.delete_schedule.side_effect = RuntimeError("redis down")

    result = await scheduler_service.remove_scheduled_task("sched-001")

    assert result["success"] is False
    assert "Failed to remove" in result["message"]


# ── list_scheduled_tasks ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_scheduled_tasks_success(scheduler_service, mock_dynamic_source):
    tasks = [
        _make_task(task_name="task_a", schedule_id="a"),
        _make_task(task_name="task_b", schedule_id="b"),
    ]
    mock_dynamic_source.get_schedules.return_value = tasks

    result = await scheduler_service.list_scheduled_tasks()

    assert result["success"] is True
    assert result["count"] == 2
    assert len(result["tasks"]) == 2
    assert result["tasks"][0]["task_name"] == "task_a"
    assert result["tasks"][1]["task_name"] == "task_b"


@pytest.mark.asyncio
async def test_list_scheduled_tasks_empty(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.get_schedules.return_value = []

    result = await scheduler_service.list_scheduled_tasks()

    assert result["success"] is True
    assert result["count"] == 0
    assert result["tasks"] == []


@pytest.mark.asyncio
async def test_list_scheduled_tasks_with_time_and_interval(scheduler_service, mock_dynamic_source):
    task = _make_task()
    task.time = datetime(2026, 6, 1, 12, 0, 0)
    task.interval = timedelta(seconds=300)
    mock_dynamic_source.get_schedules.return_value = [task]

    result = await scheduler_service.list_scheduled_tasks()

    assert result["success"] is True
    task_info = result["tasks"][0]
    assert task_info["time"] == "2026-06-01T12:00:00"
    assert task_info["interval"] is not None


@pytest.mark.asyncio
async def test_list_scheduled_tasks_error(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.get_schedules.side_effect = RuntimeError("oops")

    result = await scheduler_service.list_scheduled_tasks()

    assert result["success"] is False
    assert result["tasks"] == []
    assert result["count"] == 0


# ── get_scheduled_task ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_scheduled_task_success(scheduler_service, mock_dynamic_source):
    task = _make_task(task_name="my_task", schedule_id="sched-42")
    mock_dynamic_source.get_schedule_by_id.return_value = task

    result = await scheduler_service.get_scheduled_task("sched-42")

    assert result["success"] is True
    assert result["task_info"]["task_name"] == "my_task"
    assert result["task_info"]["schedule_id"] == "sched-42"
    mock_dynamic_source.get_schedule_by_id.assert_awaited_once_with("sched-42")


@pytest.mark.asyncio
async def test_get_scheduled_task_not_found(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.get_schedule_by_id.return_value = None

    result = await scheduler_service.get_scheduled_task("no-such-id")

    assert result["success"] is False
    assert "not found" in result["message"]
    assert result["task_info"] is None


@pytest.mark.asyncio
async def test_get_scheduled_task_error(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.get_schedule_by_id.side_effect = TypeError("bad type")

    result = await scheduler_service.get_scheduled_task("sched-42")

    assert result["success"] is False
    assert "Failed to retrieve" in result["message"]
    assert result["task_info"] is None


# ── clear_all_scheduled_tasks ───────────────────────────────────────


@pytest.mark.asyncio
async def test_clear_all_scheduled_tasks_success(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.clear_all_schedules.return_value = 5

    result = await scheduler_service.clear_all_scheduled_tasks()

    assert result["success"] is True
    assert result["cleared_count"] == 5
    assert "Cleared 5" in result["message"]


@pytest.mark.asyncio
async def test_clear_all_scheduled_tasks_none(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.clear_all_schedules.return_value = 0

    result = await scheduler_service.clear_all_scheduled_tasks()

    assert result["success"] is True
    assert result["cleared_count"] == 0


@pytest.mark.asyncio
async def test_clear_all_scheduled_tasks_error(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.clear_all_schedules.side_effect = RuntimeError("boom")

    result = await scheduler_service.clear_all_scheduled_tasks()

    assert result["success"] is False
    assert result["cleared_count"] == 0


# ── get_scheduled_task_count ────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_scheduled_task_count_async(scheduler_service, mock_dynamic_source):
    mock_dynamic_source.get_schedule_count_async = AsyncMock(return_value=7)

    count = await scheduler_service.get_scheduled_task_count()

    assert count == 7
    mock_dynamic_source.get_schedule_count_async.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_scheduled_task_count_sync_fallback(scheduler_service):
    class SyncOnlySource:
        get_schedule_count = Mock(return_value=3)

    source = SyncOnlySource()
    scheduler_service.dynamic_source = source

    count = await scheduler_service.get_scheduled_task_count()

    assert count == 3
    source.get_schedule_count.assert_called_once()
