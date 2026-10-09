import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "devsecops" / "sast" / "sample-app"))

from app import check_password, get_user, run_diagnostic


def test_get_user_handles_quotes_as_data():
    username = "demo' OR '1'='1"
    assert get_user(username) == (username,)


def test_password_hash_is_salted_and_not_plaintext():
    password = "Example-Password-For-Testing!"
    first = check_password(password)
    second = check_password(password)

    assert first != second
    assert password not in first
    salt_hex, digest_hex = first.split(":")
    assert len(bytes.fromhex(salt_hex)) == 16
    assert len(bytes.fromhex(digest_hex)) == 32


def test_diagnostic_prints_input_as_data():
    message = "assessment-safe-message"
    result = run_diagnostic(message)

    assert result.returncode == 0
    assert result.stdout == message


def test_diagnostic_does_not_execute_shell_metacharacters():
    message = "$(touch /tmp/rlogics-shell-test)"
    result = run_diagnostic(message)

    assert result.returncode == 0
    assert result.stdout == message
    assert not Path("/tmp/rlogics-shell-test").exists()
