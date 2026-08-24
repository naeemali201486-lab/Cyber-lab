from auth import verify_password, log_attempt

print("=== Authentication Security Test ===")

wrong_password = "wrong-password"

success = verify_password(wrong_password)
log_attempt(success)

print("Wrong password accepted:", success)

if not success:
    print("Failed login correctly rejected: PASS")
else:
    print("Failed login correctly rejected: FAIL")
