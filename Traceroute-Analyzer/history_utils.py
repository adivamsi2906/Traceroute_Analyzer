import os
import json
from logger_utils import setup_logger
from datetime import datetime

logger = setup_logger()

def load_latest_traceroute(target):
    results_dir = 'results'
    
    if not os.path.exists(results_dir):
        logger.warning("No previous traceroute found because the 'results' directory is missing.")
        return None

    # Get all traceroute files in the results directory
    result_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    
    if not result_files:
        logger.info("No traceroute result files found.")
        return None

    # Look for files that match the target IP
    matching_files = [f for f in result_files if target.replace('.', '_') in f]
    
    if not matching_files:
        logger.info(f"No previous traceroute found for {target}")
        return None

    # Sort the files by last modified time (most recent first)
    matching_files.sort(key=lambda f: os.path.getmtime(os.path.join(results_dir, f)), reverse=True)
    
    logger.info(f"Found {len(matching_files)} matching files for {target}. Most recent is {matching_files[0]}")

    # Select the most recent file
    most_recent_file = matching_files[0]
    file_path = os.path.join(results_dir, most_recent_file)

    try:
        # Read the JSON data from the most recent file
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded previous traceroute from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading previous traceroute from {file_path}: {e}")
        return None


def save_traceroute_to_json(target, hops):
    data = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "hops": hops
    }

    # Ensure the 'results' directory exists
    if not os.path.exists("results"):
        os.mkdir("results")

    # Format the filename with timestamp to ensure uniqueness
    filename = f"results/traceroute_{target.replace('.','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Save the traceroute data to the file
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Traceroute data saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving traceroute to {filename}: {e}")
        print(f"Error saving traceroute to {filename}: {e}")
