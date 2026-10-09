import hashlib
import os
import secrets
import sqlite3
import subprocess


def get_user(username):
    """Demonstrate parameterized SQL queries."""
    with sqlite3.connect(":memory:") as connection:
        query = "SELECT ?"
        return connection.execute(query, (username,)).fetchone()


def check_password(password):
    """Demonstrate salted password hashing with scrypt."""
    salt = secrets.token_bytes(16)
    derived_key = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
        dklen=32,
    )
    # Store both salt and derived key in a real password system.
    return f"{salt.hex()}:{derived_key.hex()}"


def run_diagnostic(message):
    """Print a message without invoking a shell."""
    return subprocess.run(
        ["/usr/bin/printf", "%s", message],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )


if __name__ == "__main__":
    username = os.getenv("LAB_USERNAME", "demo")
    print(get_user(username))
