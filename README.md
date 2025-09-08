# Traceroute Analyzer
# Traceroute Analyzer with Path History & Visualization
# This project provides an advanced **Traceroute Analyzer** that captures and compares traceroute data to diagnose network path changes, identify new hops, and monitor connectivity issues over time. The tool also generates a graphical visualization of the traceroute path for better analysis and debugging.


## Key Features:
- **Traceroute Execution**: Runs traceroutes to a specified target IP or domain (e.g., `8.8.8.8`).
- **Data Parsing**: Parses traceroute output to extract hop details (IPs, RTTs).
- **Path History**: Stores past traceroutes in JSON format and loads the most recent trace for comparison.
- **Comparison & Reporting**: Compares current and past traceroutes to identify IP changes, missing hops, or new hops.
- **Visualization**: Automatically generates a visual representation of the traceroute path as a graph.
- **Web Interface**: User-friendly interface built with Flask for real-time traceroute execution and visualization. The results are presented through an interactive web page.

## Technologies Used:
- **Python**: The backend logic, including traceroute parsing, history management, and graphing.
- **Flask**: The web framework to handle requests and serve the user interface.
- **NetworkX & Matplotlib**: Libraries for creating and displaying the traceroute path graph.
- **JSON**: For storing and retrieving historical traceroute data.

## Use Cases:
- **Network Troubleshooting**: Identify changes or issues in your network path that could be affecting performance.
- **Performance Monitoring**: Track the performance (RTTs) and reliability of network routes over time.
- **Learning & Education**: Understand the traceroute mechanism and analyze network paths.


## Getting Started:
1. Clone or download the repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Run the Flask application with `python app.py` to start the web server.
4. Visit `http://localhost:5000` in your browser to start using the tool.

### Prerequisites:
- Python 3.x

### Installation:
1. Clone or download the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/traceroute-analyzer.git

2.Navigate to the project directory:

cd traceroute-analyzer


3.Install the required dependencies using pip:

pip install -r requirements.txt

## File Structure:
The project’s file structure is organized as follows:

<img width="394" height="664" alt="image" src="https://github.com/user-attachments/assets/0f044f92-0165-491d-a483-bb739c398133" />
              
Brief project structure in short with the files usage:
<img width="980" height="630" alt="image" src="https://github.com/user-attachments/assets/1499ac9f-4340-4f49-b02e-01f5b7227306" />

**Running the Application:**

Run the Flask application:

python app.py


Open your browser and visit http://localhost:5000
 to start using the tool.

**Features in Detail:**
**Traceroute Execution:**

Execute traceroutes to any target IP address or domain (e.g., 8.8.8.8).

View hop-by-hop details, including IP addresses and RTTs.

**Path History:**

Automatically saves past traceroutes in a JSON format.

Compare the most recent traceroute with previous results to detect network changes.

**Comparison & Reporting:**

Identify if an IP has changed between traceroutes.

Detect missing or new hops in the path.

Get detailed logs and reports of the comparison results.

**Visualization:**

A graphical representation of the traceroute path is generated using NetworkX and Matplotlib.

View the traceroute as an interactive graph for better analysis.

**Requirements:**

Python 3.x

Flask: Web framework for the frontend and backend.

NetworkX: Library for creating network graphs.

Matplotlib: Plotting library to visualize traceroute paths.

Gunicorn: WSGI HTTP Server (for production use, optional).

**Testing:**

This project includes unit tests to validate the traceroute comparison and history loading functionality.

To run the tests:

python -m unittest discover

**License:**

This project is licensed under the **MIT License** - see the LICENSE
 file for details.

**Acknowledgments:**

This project was developed as part of a personal and technical learning project for learning core networking concepts, network troubleshooting and performance monitoring.

Libraries and tools used: Flask, NetworkX, Matplotlib, and Python's standard libraries.

**Additional Resources:**

Traceroute Wikipedia
 - Learn more about how traceroute works.

Flask Documentation
 - Learn more about Flask and how to build web applications in Python.
