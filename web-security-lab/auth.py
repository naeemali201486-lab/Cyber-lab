from pathlib import Path
from hashlib import pbkdf2_hmac
from secrets import token_bytes
from datetime import datetime

LOG = Path("auth.log")

USERNAME = "labuser"
PASSWORD = "LabPass123!"

salt = token_bytes(16)

password_hash = pbkdf2_hmac(
    "sha256",
    PASSWORD.encode(),
    salt,
    100_000
)

def verify_password(password):
    candidate = pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000
    )
    return candidate == password_hash

def log_attempt(success):
    status = "SUCCESS" if success else "FAILED"
    timestamp = datetime.now().isoformat(timespec="seconds")

    with LOG.open("a") as log:
        log.write(f"{timestamp} | {USERNAME} | {status}\n")

    if not success:
        soc_log = (
            Path.home()
            / "cyber-lab"
            / "logs"
            / "web-security-lab.log"
        )

        soc_log.parent.mkdir(parents=True, exist_ok=True)

        with soc_log.open("a", encoding="utf-8") as log:
            log.write(
                f"127.0.0.1 - - [{timestamp}] "
                '"AUTH /login" 401 - AUTH_FAILURE\\n'
            )

print("=== Local Authentication Test ===")

success = verify_password(PASSWORD)
log_attempt(success)

print("Password verification:", "PASS" if success else "FAIL")
print("Authentication log:", LOG)
