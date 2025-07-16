from datetime import datetime

def score_domain_profile(domain_data: dict, bid_data: dict = None) -> dict:
    item = domain_data.get("item", {})
    score = 0
    reasons = []

    # --- 1. Verified Domain (+20)
    if item.get("verified"):
        score += 20
        reasons.append("✅ Verified domain (+20)")

    # --- 2. Whitelisted Trust Level (+10)
    if item.get("trust", "").lower() == "whitelist":
        score += 10
        reasons.append("✅ Whitelisted DNS trust level (+10)")

    # --- 3. Approved by Curator (like Getgems) (+10)
    if item.get("approved_by"):
        score += 10
        reasons.append(f"✅ Approved by {', '.join(item.get('approved_by'))} (+10)")

    # --- 4. Sale Status (+10)
    if "sale" in item:
        score += 10
        reasons.append("🛍️ Listed for sale (+10)")

    # --- 5. Price Tier (+5 to +15)
    try:
        price = int(item["sale"]["price"]["value"])
        ton_value = price / (10 ** item["sale"]["price"]["decimals"])
        if ton_value < 100:
            score += 5
            reasons.append("💸 Low price: < 100 TON (+5)")
        elif ton_value < 1000:
            score += 10
            reasons.append("💸 Moderate price: 100–999 TON (+10)")
        else:
            score += 15
            reasons.append("💰 Premium price: 1000+ TON (+15)")
    except:
        pass

    # --- 6. Recent Activity (Based on Bids) (+5 to +15)
    if bid_data:
        bids = bid_data.get("data", [])
        bid_count = len(bids)
        if bid_count > 0:
            latest = max(bid.get("txTime", 0) for bid in bids)
            age_days = (datetime.utcnow().timestamp() - latest) / 86400

            score += 5  # activity bonus
            reasons.append(f"📈 {bid_count} historical bids (+5)")

            if age_days < 30:
                score += 10
                reasons.append("🕒 Recent bids in last 30 days (+10)")
            elif age_days < 90:
                score += 5
                reasons.append("📆 Active within last 90 days (+5)")

    # --- 7. Memorable or Branded Name (+10)
    name = domain_data.get("name", "")
    if name and any(keyword in name.lower() for keyword in ["wallet", "nft", "crypto", "defi", "ton", "hamster", "bot"]):
        score += 10
        reasons.append(f"📛 Memorable or brand-friendly name: '{name}' (+10)")

    # --- 8. Cap to 100
    final_score = min(score, 100)

    return {
        "score": final_score,
        "reasons": reasons
    }
