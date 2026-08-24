from time import time

MAX_ATTEMPTS = 3
WINDOW = 30

attempts = []

def allowed():
    now = time()

    while attempts and now - attempts[0] > WINDOW:
        attempts.pop(0)

    if len(attempts) >= MAX_ATTEMPTS:
        return False

    attempts.append(now)
    return True

if __name__ == "__main__":
    print("=== Rate Limit Test ===")

    for i in range(5):
        print(
            f"Attempt {i + 1}:",
            "ALLOWED" if allowed() else "BLOCKED"
        )
