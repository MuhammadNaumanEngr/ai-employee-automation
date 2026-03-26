from pathlib import Path
from datetime import datetime

vault = Path("Documents/AI_Employee_Vault")
done = vault / "Done"
briefings = vault / "Briefings"

report = briefings / f"Report_{datetime.now().date()}.md"

tasks = list(done.glob("*"))

content = "# CEO Weekly Report\n\n"

content += f"Tasks completed: {len(tasks)}\n\n"

for t in tasks:
    content += f"- {t.name}\n"

report.write_text(content)

print("Report generated.")