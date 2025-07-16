# bot.py
import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BOT_TOKEN
print(BOT_TOKEN)
from backend_client import (
    fetch_domain_analysis,
    fetch_account_info,
    resolve_domain_to_address,
    fetch_recent_transactions,
    subscribe_user
)

bot = telebot.TeleBot(BOT_TOKEN)
user_domains = {}

# 🎛 UI Buttons
def home_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 Analyze Domain", callback_data="menu:analyze"),
        InlineKeyboardButton("🎯 Check Availability", callback_data="menu:check"),
        InlineKeyboardButton("🧠 Profile Suggestion", callback_data="menu:profile"),
        InlineKeyboardButton("🔎 Account Details", callback_data="menu:account")
    )
    return markup

def domain_action_buttons(domain):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 Full Analysis", callback_data=f"analyze:{domain}"),
        InlineKeyboardButton("📈 Score Only", callback_data=f"score:{domain}"),
        InlineKeyboardButton("🧠 Summary Only", callback_data=f"summary:{domain}"),
        InlineKeyboardButton("📜 Recent TX", callback_data=f"txs:{domain}"),
        InlineKeyboardButton("🔔 Subscribe", callback_data=f"sub:{domain}"),
        InlineKeyboardButton("🏠 Back to Menu", callback_data="menu:home")
    )
    return markup

# 🔘 Start/Menu
@bot.message_handler(commands=["start", "menu"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome! Choose a tool below.",
        reply_markup=home_buttons()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("menu:"))
def handle_menu_nav(call):
    action = call.data.split(":")[1]
    messages = {
        "analyze": "🔎 Send me a domain name to analyze (e.g. `alpha.ton`)",
        "check": "🎯 (Coming soon) Check domain availability",
        "profile": "🧠 (Coming soon) Get profile suggestions for domains",
        "account": "🔍 Send the TON address you want to look up (base64 format)",
        "home": "🏠 Back to main menu:"
    }
    bot.send_message(
        call.message.chat.id,
        messages[action],
        reply_markup=home_buttons() if action == "home" else None,
        parse_mode="Markdown"
    )

# 🔠 Domain input
@bot.message_handler(func=lambda msg: is_valid_ton_domain(msg.text))
def handle_domain_input(message):
    domain = message.text.strip().lower()
    user_domains[message.chat.id] = domain
    bot.send_message(
        message.chat.id,
        f"✅ Got domain: `{domain}`. What do you want to do?",
        reply_markup=domain_action_buttons(domain),
        parse_mode="Markdown"
    )

def is_valid_ton_domain(text: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9-]+\.ton", text.strip().lower()))

# 🧾 TON account input
@bot.message_handler(func=lambda msg: is_valid_ton_address(msg.text))
def handle_ton_account(message):
    address = message.text.strip()
    bot.send_message(message.chat.id, f"⏳ Fetching account details for `{address}`...", parse_mode="Markdown")
    data = fetch_account_info(address)
    if not data:
        bot.send_message(message.chat.id, "❌ Failed to fetch account info.")
        return
    bot.send_message(message.chat.id, format_account_info(data), parse_mode="Markdown")

def is_valid_ton_address(text: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{48,64}", text.strip()))

# 📡 Domain analysis
@bot.callback_query_handler(func=lambda call: call.data.startswith(("analyze:", "score:", "summary:")))
def handle_domain_actions(call: CallbackQuery):
    action, domain = call.data.split(":", 1)
    bot.answer_callback_query(call.id, f"{action.capitalize()} for {domain}")
    bot.send_message(call.message.chat.id, f"⏳ Fetching {action} for `{domain}`...", parse_mode="Markdown")
    data = fetch_domain_analysis(domain)
    if not data:
        bot.send_message(call.message.chat.id, "❌ Failed to fetch domain analysis.")
        return
    formatters = {
        "analyze": format_full_analysis,
        "score": format_score_only,
        "summary": format_summary_only
    }
    bot.send_message(call.message.chat.id, formatters[action](data), parse_mode="Markdown")

# 🔁 Recent TX
@bot.callback_query_handler(func=lambda call: call.data.startswith("txs:"))
def handle_recent_transactions(call: CallbackQuery):
    domain = call.data.split(":", 1)[1]
    address = resolve_domain_to_address(domain)
    if not address:
        bot.send_message(call.message.chat.id, "❌ Could not resolve domain to address.")
        return
    bot.send_message(call.message.chat.id, f"📥 Getting recent TX for `{address}`...", parse_mode="Markdown")
    txs = fetch_recent_transactions(address)
    if not txs:
        bot.send_message(call.message.chat.id, "No recent transactions found.")
        return
    for tx in txs[:5]:
        bot.send_message(call.message.chat.id, format_transaction(tx), parse_mode="Markdown")

# 🔔 Subscribe
@bot.callback_query_handler(func=lambda call: call.data.startswith("sub:"))
def handle_subscribe(call: CallbackQuery):
    domain = call.data.split(":", 1)[1]
    address = resolve_domain_to_address(domain)
    if not address:
        bot.send_message(call.message.chat.id, "❌ Could not resolve domain to address.")
        return
    result = subscribe_user(call.message.chat.id, address)
    bot.send_message(call.message.chat.id, f"✅ Subscribed to `{domain}`" if result else "❌ Subscription failed.")

# 📄 Formatters
def format_full_analysis(data: dict) -> str:
    return (
        f"📊 *Domain:* `{data['domain']}`\n"
        f"🔢 *Score:* {data['score']}\n"
        f"💡 *Reasons:*\n" +
        "\n".join(f"- {r}" for r in data.get("reasons", [])) +
        f"\n\n🧠 *AI Summary:*\n{data.get('summary', '')}"
    )

def format_score_only(data: dict) -> str:
    return (
        f"📊 *Domain:* `{data['domain']}`\n"
        f"🔢 *Score:* {data['score']}\n"
        f"💡 *Reasons:*\n" +
        "\n".join(f"- {r}" for r in data.get("reasons", []))
    )

def format_summary_only(data: dict) -> str:
    return f"🧠 *AI Summary for `{data['domain']}`:*\n{data.get('summary', '')}"

def format_account_info(data: dict) -> str:
    text = f"🏦 *TON Account Info:*\n`{data.get('address', 'N/A')}`\n\n"
    if 'balance' in data:
        text += f"💰 *Balance:* {data['balance']} TON\n"
    if 'last_tx' in data:
        text += f"🔄 *Last TX:* `{data['last_tx']}`\n"
    if 'status' in data:
        text += f"📶 *Status:* {data['status']}\n"
    if 'contracts' in data:
        text += f"⚙️ *Contracts:* {', '.join(data['contracts'])}\n"
    return text

def format_transaction(tx: dict) -> str:
    return (
        f"🔁 *TX:* `{tx.get('hash', 'N/A')}`\n"
        f"📤 From: `{tx.get('source')}`\n"
        f"📥 To: `{tx.get('destination')}`\n"
        f"💰 Value: `{tx.get('value')} TON`\n"
        f"⏱ Time: {tx.get('timestamp')}\n"
    )

# 🔁 Run bot
if __name__ == "__main__":
    print("DNS Insight Bot running...")
    bot.infinity_polling()
