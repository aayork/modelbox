import json
import shlex
import subprocess
import pytest

SANDBOX = "test-sandbox"

"""This runs INSIDE the sandbox"""
def sbx_exec(command: str, timeout: int = 60) -> subprocess.CompletedProcess:
    """Run a shell command INSIDE the sandbox. `command` is passed as ONE argument.
    Safe for any input, including model output."""
    return subprocess.run(
        ["sbx", "exec", SANDBOX, "sh", "-c", command],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )

"""This runs on the host"""
def sbx(args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    """Run an sbx CLI command on the HOST (e.g. "policy log ...").
    Only for fixed strings written in this file, never model output."""
    return subprocess.run(
        ["sbx", *shlex.split(args)],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )

"""Initialize the sandbox"""
@pytest.fixture(scope="module")
def running_sandbox():
    sbx_exec("true")

def test_exit_code_passes_through(running_sandbox):
    r = sbx_exec("echo out; echo err >&2; exit 3")
    assert r.returncode == 3
    assert r.stdout == "out\n"
    assert r.stderr == "err\n"

def test_where_am_i():
    r = sbx_exec("pwd; ls")
    print(r.stdout)
