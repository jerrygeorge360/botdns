# 🧠 DNS Insight Bot for TON

A powerful Telegram bot that provides analysis, scoring, and insights for `.ton` domains and TON blockchain addresses.



## 📌 Features

* 🔍 **Domain Analysis** – Analyze `.ton` domains and get a score with AI-generated reasons and summaries.
* 🎯 **Domain Availability** *(Coming Soon)* – Check if a domain is available for registration.
* 🧠 **Profile Suggestion** *(Coming Soon)* – Get profile suggestions for domains.
* 🔎 **TON Address Info** – Fetch and display TON account details by address.
* 📜 **Recent Transactions** – View the last few transactions of any resolved domain.
* 🔔 **Subscription** – Subscribe to domain updates.

---

## 🛠️ Tech Stack

* **Python** + **Flask** – API backend
* **Telebot (pyTelegramBotAPI)** – Telegram bot integration
* **Grok or LLM** – AI summary generation
* **TON API** – TON blockchain data
* **dotenv** – Configuration handling
* **JSON-based storage** – For lightweight subscriptions
* **Emoji Plugins** – "Yet another emoji support"

---

## 🚀 How It Works

### 1. User starts the bot:

```bash
/start
```

### 2. The bot presents an inline menu:

* Analyze a domain (`example.ton`)
* View score, AI summary, or recent transactions
* Get wallet/account details

### 3. Bot interacts with Flask backend APIs like:

* `/analyze/<domain>` → for scoring + AI summary
* `/resolve/<domain>` → resolve `.ton` domain to address
* `/accounts/<address>` → fetch account info
* `/ai/analyze/<domain>` → call GROK to analyze domain detail

---

## 📦 Project Structure

```
📁 dnsbot/
├── bot             # Main Telegram bot logic
├── backend           # backend logic and routes
├─services            # different services(LLM service,)
├── utils/              # helpers and logger
│
├── README.md
├── .env                # Secrets & API keys
```

---

## 🔐 Environment Variables

Create a `.env` file with:

```env
INSIGHT_API_BASE=http://localhost:5000 or wherever you are hosting it
TON_API_TOKEN=<your-tonapi-token>
TON_API_BASE=https://tonapi.io
GROQ_KEY=<your-grok-token>
TG_API_TOKEN=<your-bot-token>
```

---

## ⚙️ Run the Bot and Backend

### 1. Start Flask API (Backend):

```bash
python app.py
```

### 2. Run the Telegram Bot:

```bash
python bot.py
```

Make sure both are running concurrently.

---

## 📋 Sample Bot Commands

```bash
/start
/menu
```

Then enter:

```
alpha.ton
```

Or directly send:

```
EQBlahBlah... (TON address)
```

---

## 🧪 Sample `/analyze/<domain>` Output

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

Built by Jerry George (@jerrygeorge360) for TON ecosystem analysis and developer tools.

---

## 📄 License.
MIT