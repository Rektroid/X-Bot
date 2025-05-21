# REKTroid Bot

REKTroid is a savage AI bot that roasts crypto and degen communities using X (Twitter) data and LLMs. It runs across:

* 🧠 Sentiment-aware roasts from X (via Tweepy)
* 🤖 Discord bot for command control
* 🔁 Hourly roast scheduler
* 🧵 LLM-based insults (via OpenRouter)

---

## 🔧 Features

* Auto-posts crypto roasts to X every hour
* Accepts `/roast`, `/roast_post`, and `/roast_llm` commands in Discord
* Logs status and crashes to a Discord webhook
* Sentiment-aware phrase extraction from X
* Roast history tracked in `roast_history.jsonl`

---

## 🗂 Project Structure

```
rektroid/
├── rektroid_bot.py       # Core bot logic
├── rektroid_api.py       # Optional Flask API
├── discord_bot.py        # Discord bot with commands
├── scheduler.py          # Hourly auto-roast poster
├── requirements.txt
└── .env                  # Secrets (not committed)
```

---

## 🔐 Environment Variables

| Key                        | Purpose                 |
| -------------------------- | ----------------------- |
| `API_KEY`                  | X/Twitter API key       |
| `API_SECRET`               | X/Twitter API secret    |
| `ACCESS_TOKEN`             | X/Twitter access token  |
| `ACCESS_TOKEN_SECRET`      | X/Twitter access secret |
| `OPENROUTER_API_KEY`       | OpenRouter LLM API key  |
| `DISCORD_BOT_TOKEN`        | Discord bot token       |
| `DISCORD_ADMIN_CHANNEL_ID` | Channel ID to report to |
| `DISCORD_LOG_WEBHOOK`      | Webhook for crash logs  |

Add these in Railway under **Variables** tab.

---

## 🚀 Deployment on Railway

1. Push this repo to GitHub
2. Create a new Railway project → "Deploy from GitHub"
3. Add secrets (env vars)
4. Add two services:

   * `python discord_bot.py`
   * `python scheduler.py`

*(optional)* Add `rektroid_api.py` if you want HTTP endpoints

---

## 💬 Discord Commands

| Command                   | Description                             |
| ------------------------- | --------------------------------------- |
| `!roast [community]`      | Generate roast from templates/sentiment |
| `!roast_post [community]` | Generate and post roast to X            |
| `!roast_llm [community]`  | Generate roast from LLM (OpenRouter)    |

---

## 🧠 Auto-Roasting Scheduler

* Runs every 1 hour ± 10 mins
* Picks random community from templates
* Posts roast to X
* Logs result to Discord via webhook

---

## 🧪 Testing

* You can test `rektroid_bot.py` manually
* Add mocks for `tweepy` and API keys if testing offline

---

## 📜 License

MIT License. Use responsibly — especially with live posting and profanity. Your bot, your rules (and risks).
