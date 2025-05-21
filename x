#!/usr/bin/env uv run --script
from subprocess import run
from _task.task import task, runner

@task(description="Run Google ADK server")
def web():
    run(["uv", "run", "adk", "web", "agents"])

if __name__ == "__main__":
    runner()
