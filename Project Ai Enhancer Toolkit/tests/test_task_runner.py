
import sys
from pathlib import Path

from threading import Event

import pytest


APP_SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_SOURCE))

from frontend.task_runner import TaskRunner


def test_task_runner_returns_successful_result():
    runner = TaskRunner()

    runner.run(
        "test_task",
        lambda: "completed",
    )

    task_name, result, error = runner.results.get(timeout=2)

    assert task_name == "test_task"
    assert result == "completed"
    assert error is None


def test_task_runner_passes_arguments_and_keyword_arguments():
    runner = TaskRunner()

    def calculate(first, second, multiplier=1):
        return (first + second) * multiplier

    runner.run(
        "calculation",
        calculate,
        5,
        3,
        multiplier=2,
    )

    task_name, result, error = runner.results.get(timeout=2)

    assert task_name == "calculation"
    assert result == 16
    assert error is None


def test_task_runner_returns_exception():
    runner = TaskRunner()

    def failing_task():
        raise ValueError("Test failure")

    runner.run(
        "failing_task",
        failing_task,
    )

    task_name, result, error = runner.results.get(timeout=2)

    assert task_name == "failing_task"
    assert result is None
    assert isinstance(error, ValueError)
    assert str(error) == "Test failure"


def test_task_runner_does_not_block_calling_thread():
    runner = TaskRunner()
    task_started = Event()
    release_task = Event()

    def background_task():
        task_started.set()
        release_task.wait(timeout=2)
        return "finished"

    try:
        # Keep the worker unfinished while checking that run() returned.
        runner.run("background_task", background_task)

        assert task_started.wait(timeout=1)
        assert runner.results.empty()
    finally:
        release_task.set()

    task_name, result, error = runner.results.get(timeout=2)
    assert task_name == "background_task"
    assert result == "finished"
    assert error is None
