# 🧠 DNS Insight Bot for TON

A powerful Telegram bot and API that provides analysis, scoring, and insights for `.ton` domains and TON blockchain addresses.

---

## 📌 Features

- 🔍 **Domain Analysis** – Analyze `.ton` domains and get a score with AI-generated reasons and summaries.
- 🔎 **TON Address Info** – Fetch and display TON account details by address.
- 📜 **Recent Transactions** – View recent transactions of any resolved domain.
- 🔔 **Subscription** – Subscribe to domain updates *(stored locally for now)*.
- 🎯 **Domain Availability** *(Coming Soon)*
- 🧠 **Profile Suggestion** *(Coming Soon)*

---

## 🛠️ Tech Stack

- **Python** + **Flask** – API backend
- **Telebot (pyTelegramBotAPI)** – Telegram bot integration
- **Grok or LLM API** – AI-powered domain scoring and summaries
- **TON API** – Fetch blockchain/account data
- **dotenv** – Configuration management
- **Supervisor** – Runs both Flask + bot inside Docker container
- **Docker** – Containerized deployment

---

## 📦 Project Structure

```

📁 dnsbot/
├── backend/           # Flask API (app.py, routes/)
├── bot/               # Telegram bot logic (bot.py)
├── services/          # External API services (TON, AI/Grok)
├── utils/             # Logger, helpers
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker container config
├── supervisord.conf   # Runs both services
├── .env               # Secrets & tokens
└── README.md

````

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
INSIGHT_API_BASE=http://localhost:8080  # Will change when deployed
TON_API_TOKEN=<your-tonapi-token>
TON_API_BASE=https://tonapi.io
GROQ_KEY=<your-grok-token>
TG_API_TOKEN=<your-telegram-bot-token>
````

> ✅ `INSIGHT_API_BASE` should point to your backend API.
>
> Use `http://localhost:8080` locally, or update it to your deployed URL like `https://yourapp.fly.dev` when live.

---

## 🐳 Dockerized Setup (Flask + Bot Together)

### 1. Build the image

```bash
sudo docker build -t dnsbot .
```

### 2. Run the container

```bash
sudo docker run -p 8080:8080 --env-file .env dnsbot
```

This will:

* Start the Flask backend at `http://localhost:8080`
* Start the Telegram bot in the background (uses long polling)

### 3. Logs

To view logs:

```bash
sudo docker ps           # get container ID
sudo docker logs -f <container_id>
```

---

## 🔁 How It Works

### 1. User starts the bot:

```bash
/start
```

### 2. The bot shows a menu:

* Analyze domain (e.g. `example.ton`)
* View AI score, reasons, and summaries
* Check wallet/account details

### 3. Bot uses the backend API:

* `/api/analyze/<domain>` → AI scoring
* `/api/resolve/<domain>` → resolve domain to address
* `/api/accounts/<address>` → account info from TON
* `/api/ai/analyze/<domain>` → LLM analysis (Grok)

---

## 🧪 Sample Output

### `/api/analyze/alpha.ton`:

```json
{
  "domain": "alpha.ton",
  "score": 82,
  "reasons": [
    "High bidding activity",
    "Recently transferred ownership",
    "Belongs to a popular DNS collection"
  ],
  "summary": "Alpha.ton is a premium domain actively traded in the TON ecosystem. Based on its bidding volume and ownership status, it's a strong brand candidate."
}
```

---

## 🧑‍💻 Author

Built by [Jerry George](https://t.me/jerrygeorge360) for the TON ecosystem and the future of decentralized identity.

---

## 📄 License

MIT License.

```
