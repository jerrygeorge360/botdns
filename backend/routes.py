from flask import Blueprint, jsonify,request
from backend.services.dns_service import get_resolve_dns, get_detail_dns, get_dns_bids, get_account_info
from backend.utils.helper import (format_dns_detail_insight_input, format_dns_resolve_input_1, format_dns_bids_input)
from backend.services.llmservice.ai_service import generate_summary
from backend.services.llmservice.instructions import domain_profiler
from backend.services.score_service import score_domain_profile
bp = Blueprint('ai_insights', __name__, url_prefix='/ai')


@bp.route("/analyze/<domain>", methods=["GET"])
def analyze_domain(domain):

    # Get raw data
    detail = get_detail_dns(domain)
    bids = get_dns_bids(domain)
    score_data = score_domain_profile(detail, bids)
    # Format for AI

    text_block = "\n\n".join([
        format_dns_detail_insight_input(detail),
        format_dns_bids_input(bids)
    ])

    # Generate domain profiler
    result = generate_summary(
        text_block, domain_profiler
    )
    return jsonify({
        "domain": domain,
        "score": score_data["score"],
        "reasons": score_data["reasons"],
        "summary": result.read()}) if result else ({"error": "AI failed"}, 500)

@bp.route("/resolve/<domain>", methods=["GET"])
def resolve_domain(domain):
    try:
        data = get_resolve_dns(domain)
        if not data or "address" not in data:
            return jsonify({"error": "Domain resolution failed"}), 404
        return jsonify(format_dns_resolve_input_1(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("accounts/<address>")
def account_details(address):
    return jsonify(get_account_info(address))
