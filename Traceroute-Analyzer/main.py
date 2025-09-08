from logger_utils import setup_logger
from parser import parse_tracert_output
from traceroute_runner import run_traceroute, save_traceroute_to_json
from history_utils import load_latest_traceroute
from visualize import visualize_traceroute
from compare_utils import compare_traceroutes
import re
import sys

logger = setup_logger()

def is_valid_ip_or_domain(target):
    # Simple regex check for IP or domain
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    domain_pattern = r"^(?!\-)(?:[a-zA-Z0-9\-]{1,63}(?<!\-)\.)+[a-zA-Z]{2,}$"
    return re.match(ip_pattern, target) or re.match(domain_pattern, target)

def main():
    target = input("Enter a destination IP or domain (e.g., 8.8.8.8): ").strip()

    # ✅ Input validation
    if not is_valid_ip_or_domain(target):
        logger.error("❌ Invalid IP address or domain format.")
        sys.exit(1)

    # ✅ Traceroute execution
    output = run_traceroute(target)

    if not output or not output.strip():
        logger.error("❌ No traceroute output received. Please check your connection or input.")
        return

    parsed = parse_tracert_output(output)

    if not parsed:
        logger.warning("⚠️ No valid hops were parsed. Aborting further steps.")
        return

    logger.info("\n--- Traceroute Parsed Output ---\n")
    for hop in parsed:
        logger.info(f"Hop {hop['hop']:>2} → IP: {hop['ip']:15}  RTTs: {hop['rtts']}")

    save_traceroute_to_json(target, parsed)

    # ✅ Compare with previous if exists
    previous = load_latest_traceroute(target)
    if previous:
        logger.info(f"📁 Loaded previous traceroute to {target} from {previous['timestamp']}")
        logger.info(f"🔢 {len(previous['hops'])} hops recorded previously.")
        logger.info("\n🔍 Comparison with Previous Traceroute")
        compare_traceroutes(previous, {
            "target": target,
            "hops": parsed
        })
    else:
        logger.info("\nℹ️ No previous traceroute found — nothing to compare yet.")

    # ✅ Visualize result
    visualize_traceroute({
        "target": target,
        "hops": parsed
    })

if __name__ == "__main__":
    main()