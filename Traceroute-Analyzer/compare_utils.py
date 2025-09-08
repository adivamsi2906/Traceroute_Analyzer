from logger_utils import setup_logger
logger = setup_logger()

def compare_traceroutes(old_data, new_data):
    # Ensure both old_data and new_data are valid and contain 'hops' field
    old_hops = {hop["hop"]: hop for hop in old_data.get("hops", []) if "hop" in hop}
    new_hops = {hop["hop"]: hop for hop in new_data.get("hops", []) if "hop" in hop}

    logger.debug(f"Old Hops: {old_hops}")
    logger.debug(f"New Hops: {new_hops}")

    # Ensure there are hops to compare
    if not old_hops and not new_hops:
        logger.info("No hops to compare. Both traceroutes have no hops.")
        return "No hops to compare."

    # Determine the maximum number of hops
    max_hops = max(max(old_hops.keys(), default=0), max(new_hops.keys(), default=0))

    changes_found = False

    # Loop through each hop
    for i in range(1, max_hops + 1):
        old = old_hops.get(i)
        new = new_hops.get(i)

        if not old and new:
            logger.info(f"🆕 Hop {i}: NEW hop appeared → {new.get('ip', 'N/A')} {new.get('rtts', 'N/A')}")
            changes_found = True
        elif old and not new:
            logger.info(f"❌ Hop {i}: Previously existed but now missing → {old.get('ip', 'N/A')}")
            changes_found = True
        elif old and new:
            ip_changed = old.get("ip") != new.get("ip")
            rtt_changed = old.get("rtts") != new.get("rtts")

            if ip_changed:
                logger.info(f"🔄 Hop {i}: IP changed → {old.get('ip', 'N/A')} → {new.get('ip', 'N/A')}")
                changes_found = True
            elif rtt_changed:
                logger.info(f"⏱ Hop {i}: RTT changed → {old.get('rtts', 'N/A')} → {new.get('rtts', 'N/A')}")
                changes_found = True

    if not changes_found:
        logger.info("✅ No changes in path. The route is the same.")
        return "✅ No changes in path. The route is the same."
    return "Changes detected in the traceroute."

"""from logger_utils import setup_logger
logger = setup_logger()

def compare_traceroutes(old_data, new_data):
    old_hops = {hop["hop"]: hop for hop in old_data.get("hops", [])}
    new_hops = {hop["hop"]: hop for hop in new_data.get("hops", [])}

    logger.debug(f"Old Hops: {old_hops}")
    logger.debug(f"New Hops: {new_hops}")

    max_hops = max(max(old_hops.keys(), default=0), max(new_hops.keys(), default=0))

    changes_found = False

    for i in range(1, max_hops + 1):
        old = old_hops.get(i)
        new = new_hops.get(i)

        if not old and new:
            logger.info(f"🆕 Hop {i}: NEW hop appeared → {new['ip']} {new['rtts']}")
            changes_found = True
        elif old and not new:
            logger.info(f"❌ Hop {i}: Previously existed but now missing → {old['ip']}")
            changes_found = True
        elif old and new:
            ip_changed = old["ip"] != new["ip"]
            rtt_changed = old["rtts"] != new["rtts"]

            if ip_changed:
                logger.info(f"🔄 Hop {i}: IP changed → {old['ip']} → {new['ip']}")
                changes_found = True
            elif rtt_changed:
                logger.info(f"⏱ Hop {i}: RTT changed → {old['rtts']} → {new['rtts']}")
                changes_found = True

    if not changes_found:
        logger.info("✅ No changes in path. The route is the same.")
"""
