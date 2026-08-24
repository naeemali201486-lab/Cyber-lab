import time
import subprocess

while True:
    print("\033[2J\033[H", end="")
    subprocess.run(["python", "monitor.py"])
    print("\nNext check in 10 seconds...")
    time.sleep(10)
