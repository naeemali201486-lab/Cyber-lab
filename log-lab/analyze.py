from pathlib import Path

log_file = Path("access.log")

total = 0
success = 0
errors = 0

for line in log_file.read_text().splitlines():
    total += 1

    if "HTTP 200" in line:
        success += 1
    elif "HTTP 404" in line:
        errors += 1

print("Total requests:", total)
print("Successful:", success)
print("404 errors:", errors)
