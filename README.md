# 🧠 Ghajini — The AI That Never Forgets

> *Ghajini forgot everything in 15 minutes. This bot remembers everything forever.*

A personal AI assistant that lives on Telegram. It remembers your goals, tracks your tasks, sends you reminders, and briefs you every morning — without you having to repeat yourself every time.

---

## What It Does

```
You: "I have an interview at Zepto this Friday at 2pm"
Ghajini: Got it boss. I'll remind you before it's time.

[Friday 2pm]
Ghajini: ⏰ Reminder: Interview at Zepto. Lock in. 💪

[Next morning, 9am — automatically]
Ghajini: ☀️ Good morning boss!
         📋 Pending tasks: 2
         🎯 Active goals: 1
         → Interview at Zepto by Friday 2pm
         → Submit assignment by Thursday
         Let's get it 💪
```

No prompting. No re-explaining. It just knows.

---

## The Multi-Agent Architecture

```
Your Telegram message
        ↓
   ROUTER AGENT
   classifies the message
        ↓
┌───────┬────────┬────────┐
↓       ↓        ↓        ↓
MEMORY  TASK    GOAL    COACH
AGENT   AGENT   AGENT   AGENT
  ↓       ↓        ↓        ↓
Chroma  tasks   goals   advice
DB      .json   .json   from all
        ↓        ↓        ↓
└───────┴────────┴────────┘
        ↓
  RESPONSE AGENT
  synthesizes everything
        ↓
  Telegram reply
```

Six specialized agents. Each with one job. None knowing what the others do.

---

## Features

- **Persistent memory** — remembers facts about you across sessions using Mem0 + Chroma
- **Task tracking** — extracts deadlines and saves them automatically
- **Goal tracking** — tracks your long-term ambitions
- **Smart reminders** — actually pings you at the right time
- **Morning briefing** — automatic 9am summary of your day
- **Coach agent** — gives personalised advice based on your full context
- **`/done` command** — mark tasks as complete
- **`*` prefix** — force save anything to memory instantly

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Gemini 2.5 Flash |
| Memory extraction | Mem0 |
| Vector database | Chroma (local) |
| Embeddings | Google Gemini Embedding |
| Scheduler | APScheduler |
| Interface | Telegram Bot API |

---

## Setup — 5 Steps

**1. Clone the repo**
```bash
git clone https://github.com/yourname/ghajini
cd ghajini
```

**2. Create virtual environment**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
python -m pip install langchain langchain-google-genai langgraph python-dotenv mem0ai chromadb python-telegram-bot google-genai apscheduler
```

**4. Set up environment variables**
```bash
# .env
GOOGLE_API_KEY=your_google_ai_studio_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TIMEZONE=Asia/Kolkata
```

Get your Google API key at aistudio.google.com
Create a Telegram bot via @BotFather

**5. Run**
```bash
python main.py
```

Message your bot on Telegram. It's alive.

---

## Commands

| Command | What it does |
|---|---|
| Any message | Ghajini responds with full context |
| `* I prefer bullet points` | Force save to memory |
| `/done interview` | Mark task as completed |

---

## How Memory Works

```
You say something memorable
        ↓
Memory agent extracts key facts
        ↓
Mem0 converts to embeddings via Gemini
        ↓
Stored in local Chroma vector DB
        ↓
Every future message → relevant memories fetched
        ↓
Response agent uses them without you repeating yourself
```

Your memories live on your machine. Nobody else's server. Full privacy.

---

## Project Structure

```
ghajini/
│
├── .env                    # API keys
├── state.py                # GhajiniState TypedDict
├── graph.py                # LangGraph wiring
├── bot.py                  # Telegram bot + scheduler
├── main.py                 # entry point
├── reminders.py            # scheduler + morning briefing
│
├── agents/
│   ├── router.py           # classifies messages
│   ├── memory.py           # stores and retrieves facts
│   ├── task.py             # manages todos and deadlines
│   ├── goal.py             # tracks long term goals
│   ├── coach.py            # gives personalised advice
│   └── response.py        # writes the final reply
│
├── memory/
│   └── store.py            # Mem0 + Chroma wrapper
│
└── data/
    ├── tasks.json          # your tasks
    ├── goals.json          # your goals
    └── chat_ids.json       # your telegram chat id
```

---

## Cost

Everything is free.
- Gemini API → free tier (1500 calls/day)
- Telegram API → completely free
- Chroma → local, free
- Mem0 OSS → self-hosted, free
- APScheduler → open source, free

---

## The Name

Ghajini is a Bollywood film about a man who forgets everything every 15 minutes.

This bot is the opposite.

---

*Built with LangGraph + Gemini. Your second brain on Telegram.*