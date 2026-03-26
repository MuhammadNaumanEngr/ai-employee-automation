import os
import time
import shutil
import logging
import subprocess
from pathlib import Path

# Setup
vault = Path.home() / "Documents" / "AI_Employee_Vault"
needs_action = vault / "Needs_Action"
approval    = vault / "Pending_Approval"
plans       = vault / "Plans"
done        = vault / "Done"

for d in [needs_action, approval, plans, done]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(vault / "orchestrator.log"),
              logging.StreamHandler()]
)
log = logging.getLogger(__name__)

def process_task(task: Path) -> None:
    try:
        content = task.read_text()
    except OSError as e:
        log.error("Cannot read %s: %s", task.name, e)
        return

    # Gate: send payment tasks for human approval
    if "payment" in content.lower():
        dest = approval / task.name
        shutil.move(str(task), dest)
        log.info("Held for approval: %s", task.name)
        return                          # ← stop here, don't process further

    log.info("Processing: %s", task.name)
    try:
        subprocess.run(
    f'ccr code "Read the task file {task} and create a step by step plan in {plans} folder."',
    shell=True,
    check=True,
    cwd=str(vault),   # ← run from vault directory so ccr can find context
)
    except subprocess.CalledProcessError as e:
        log.error("ccr failed for %s: %s", task.name, e)
        return

    shutil.move(str(task), done / task.name)
    log.info("Done: %s", task.name)

log.info("Orchestrator started. Watching %s", needs_action)
while True:
    for task in list(needs_action.glob("*")):
        if task.is_file():              # skip any accidental subdirs
            process_task(task)
    time.sleep(60)