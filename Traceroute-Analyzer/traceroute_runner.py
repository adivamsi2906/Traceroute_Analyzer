import subprocess
import platform
from datetime import datetime
import os
import json
import time
from logger_utils import setup_logger

logger = setup_logger()


def run_traceroute(host: str) -> str:
    system_platform = platform.system().lower()

    if system_platform == "windows":
        command = ["tracert", host]
    else:
        command = ["traceroute", "-n", host]

    logger.info(f"🚀 Running command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            logger.error(f"[!] Traceroute command failed: {result.stderr.strip()}")
        return result.stdout

    except subprocess.TimeoutExpired:
        logger.error("❌ Traceroute command timed out.")
        return ""

    except Exception as e:
        logger.exception(f"❌ Unexpected error while running traceroute: {e}")
        return ""
    
def save_traceroute_to_json(target, hops):
    os.makedirs("results", exist_ok=True)
    filename = f"results/traceroute_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "hops": hops
    }

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Traceroute saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving traceroute: {e}")