from pathlib import Path

log = Path("monitor.log").read_text().splitlines()

checks = []
current = None

for line in log:
    if line.startswith("=== Check "):
        current = {"time": line[9:-3]}
        checks.append(current)
    elif line.startswith("Overall:") and current:
        current["status"] = line.split(":", 1)[1].strip()

total = len(checks)
passed = sum(c.get("status") == "PASS" for c in checks)
failed = sum(c.get("status") == "FAIL" for c in checks)

print("=== Central Monitor Report ===")
print(f"Total checks: {total}")
print(f"PASS checks: {passed}")
print(f"FAIL checks: {failed}")

if checks:
    print(f"Latest status: {checks[-1].get('status', 'UNKNOWN')}")

print("Overall:", "HEALTHY" if checks and checks[-1].get("status") == "PASS" else "ATTENTION REQUIRED")
