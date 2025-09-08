from flask import Flask, render_template, request, session, url_for
from traceroute_runner import run_traceroute, save_traceroute_to_json
from parser import parse_tracert_output
from history_utils import load_latest_traceroute
from compare_utils import compare_traceroutes
from visualize import visualize_traceroute
import logging
import os

# Setup logger
def setup_logger(log_file="logs/app.log"):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("TracerouteLogger")
    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

logger = setup_logger()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add your secret key

@app.route('/')
def index():
    # Initialize variables for GET request (first page load)
    traceroute_output = ""
    comparison_output = ""
    target = ""
    
    return render_template('index.html', traceroute_output=traceroute_output, comparison_output=comparison_output, target=target)

@app.route('/traceroute', methods=['POST'])
def traceroute():
    target = request.form['target']
    if not target:
        return render_template('index.html', error="Please enter a valid target IP or domain.")
    
    # Store the target in session
    session['target'] = target

    # Run the traceroute command
    output = run_traceroute(target)
    if not output:
        return render_template('index.html', error="Traceroute failed. Please try again later.")

    # Parse the traceroute output
    parsed = parse_tracert_output(output)

    # Save current traceroute to JSON
    save_traceroute_to_json(target, parsed)

    # Load previous traceroute for comparison
    previous = load_latest_traceroute(target)
   
    # Compare with the previous traceroute, if available
    comparison_result = ""
    if previous:
        comparison_result = compare_traceroutes(previous, {"target": target, "hops": parsed})

    return render_template('index.html', target=target, hops=parsed, comparison=comparison_result, traceroute_output=output, comparison_output=comparison_result)

# Modify the visualize function to pass the entire traceroute_data dictionary

@app.route('/visualize', methods=['GET'])
def visualize():
    target_ip = session.get('target')  # Get the target IP from the session or elsewhere
    traceroute_data = load_latest_traceroute(target_ip)  # Load the traceroute data

    if traceroute_data:
        # Generate the graph (this step will save the image to static/traceroute_graph.png)
        visualize_traceroute(traceroute_data, filename="static/traceroute_graph.png")
        
        # After generating the graph, pass the image URL and traceroute output to the template
        traceroute_output = "Visualization Completed Sucessfully"
        return render_template('index.html', graph_url=url_for('static', filename='traceroute_graph.png'), traceroute_output=traceroute_output)
    else:
        traceroute_output = "No previous traceroute data available"
        return render_template('index.html', traceroute_output=traceroute_output)



if __name__ == "__main__":
    app.run(debug=True)
