import time
from pathlib import Path

vault = Path.home() / "Documents" / "AI_Employee_Vault"

needs_action = vault / "Needs_Action"
watch_folder = vault / "watch_folder"

watch_folder.mkdir(exist_ok=True)
needs_action.mkdir(exist_ok=True)

print("🚀 Watcher started...")

while True:
    for file in watch_folder.glob("*"):
        if file.is_file():
            dest = needs_action / file.name
            file.rename(dest)
            print("Moved:", file.name)

    time.sleep(5)