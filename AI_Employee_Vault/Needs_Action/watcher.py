import time
from pathlib import Path

watch = Path("watch_folder")
needs_action = Path("Needs_Action")

watch.mkdir(exist_ok=True)

print("Watcher running...")

while True:

    for file in watch.glob("*"):

        destination = needs_action / file.name
        file.rename(destination)

        print("New task detected:", file.name)

    time.sleep(5)