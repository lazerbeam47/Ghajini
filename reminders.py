import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler


TASKS_PATH = "data/tasks.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Asia/Kolkata"))
async def morning_briefing(bot):
    # load chat_id
    try:
        with open("data/chat_ids.json", "r") as f:
            chat_id = json.load(f)['chat_id']
    except FileNotFoundError:
        print("No chat_id found — user hasn't messaged yet")
        return
    
    # load tasks and goals
    tasks = load_tasks()
    
    try:
        with open("data/goals.json", "r") as f:
            goals = json.load(f)
    except FileNotFoundError:
        goals = []
    
    pending = [t for t in tasks if not t.get('completed')]
    
    # format message
    task_lines = "\n".join([f"→ {t['task']} by {t['date']}" 
                             for t in pending]) or "No pending tasks 🎉"
    
    message = f"""☀️ Good morning boss!

📋 Pending tasks: {len(pending)}
🎯 Active goals: {len(goals)}

Your tasks:
{task_lines}

Let's get it 💪"""
    
    await bot.send_message(chat_id=chat_id, text=message)

def load_tasks():
    if not os.path.exists(TASKS_PATH):
        return []
    with open(TASKS_PATH, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_PATH), exist_ok=True)
    with open(TASKS_PATH, "w") as f:
        json.dump(tasks, f, indent=2)


def parse_task_datetime(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return None


async def check_reminders(bot):
    tasks = load_tasks()
    now = datetime.now(TIMEZONE).replace(tzinfo=None)
    changed = False

    for task in tasks:
        if task.get("completed") or task.get("reminded_at"):
            continue

        user_id = task.get("user_id")
        reminder_at = parse_task_datetime(task.get("date"))
        if not user_id or not reminder_at or reminder_at > now:
            continue

        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"Reminder: {task.get('task', 'You asked me to remind you.')}",
            )
            task["completed"] = True
            task["reminded_at"] = now.strftime(DATE_FORMAT)
            changed = True
        except Exception as exc:
            print(f"Failed to send reminder for task {task}: {exc}")

    if changed:
        save_tasks(tasks)

def mark_task_done(keyword: str) -> str:
    tasks = load_tasks()
    found = False
    for task in tasks:
        if keyword.lower() in task['task'].lower():
            task['completed'] = True
            found = True
    save_tasks(tasks)
    return "✅ Done!" if found else "❌ Task not found"

def start_reminder_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        check_reminders,
        "interval",
        minutes=1,
        args=[bot],
        id="check_reminders",
        replace_existing=True,
        next_run_time=datetime.now(TIMEZONE),
    )
    scheduler.add_job(
    morning_briefing,
    "date",
    run_date=datetime.now(TIMEZONE),
    args=[bot],
    id="morning_briefing",
    replace_existing=True,
    )
    scheduler.start()
    return scheduler
