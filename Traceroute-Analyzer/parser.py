import re
from logger_utils import setup_logger

logger = setup_logger()

def parse_tracert_output(output: str):
    hops = []

    for line in output.splitlines():
        line = line.strip()

        # Skip lines that don't start with a hop number
        if not re.match(r"^\d+", line):
            continue

        try:
            parts = line.split()
            hop_num = int(parts[0])

            # Extract RTTs (e.g., 9 ms, 13 ms)
            rtts = re.findall(r"(\d+)\s*ms", line)
            rtts = list(map(int, rtts)) if rtts else ["*", "*", "*"]

            # Try to find IP address
            ip_match = re.search(r"\[(\d{1,3}(?:\.\d{1,3}){3})\]", line)
            if not ip_match:
                ip_match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", line)

            ip_address = ip_match.group(1) if ip_match else None

           
            if not ip_address:
                ip_address = "*"

            hops.append({
                "hop": hop_num,
                "ip": ip_address,
                "rtts": rtts
            })
        except Exception as e:
            logger.warning(f"Failed to parse line: {line}")
            logger.warning(f"Error: {e}")
            continue

    return hops