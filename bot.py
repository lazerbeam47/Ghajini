from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import json
from graph import app as graph_app
from reminders import start_reminder_scheduler, mark_task_done
from agents.task import load_tasks
from agents.goal import load_goals

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def load_chat_id():
    with open("data/chat_ids.json", "r") as f:
        return json.load(f)['chat_id']

def format_tasks(tasks):
    if not tasks:
        return "No pending tasks 🎉"
    return "\n".join([f"→ {t['task']} by {t['date']}" for t in tasks])

async def on_startup(application: Application):
    application.bot_data["reminder_scheduler"] = start_reminder_scheduler(application.bot)

async def on_shutdown(application: Application):
    scheduler = application.bot_data.get("reminder_scheduler")
    if scheduler:
        scheduler.shutdown(wait=False)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    message = update.message.text
    user_id = str(update.message.from_user.id)
    os.makedirs("data", exist_ok=True)
    with open("data/chat_ids.json", "w") as f:
        json.dump({"chat_id": chat_id}, f)
    initial_state = {
        "message": message,
        "user_id": user_id,
        "router_decision": [],
        "retrieved_memories": [],
        "agent_outputs": {},
        "final_response": ""
    }
    print("invoking graph with state:", initial_state)
    result = graph_app.invoke(initial_state)
    print("graph result:", result)
    await update.message.reply_text(result['final_response'])

async def done_command(update, context):
    keyword = " ".join(context.args)
    if not keyword:
        await update.message.reply_text("Usage: /done <task keyword>\nExample: /done interview")
        return
    result = mark_task_done(keyword)
    await update.message.reply_text(result)

# build app
app = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .post_init(on_startup)
    .post_shutdown(on_shutdown)
    .build()
)

# add handlers
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("done", done_command))

# run
app.run_polling()
