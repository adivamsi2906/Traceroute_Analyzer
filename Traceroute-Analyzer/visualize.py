import networkx as nx
import matplotlib.pyplot as plt
from logger_utils import setup_logger

logger = setup_logger()

def visualize_traceroute(traceroute_data, filename=None):
    hops = traceroute_data.get("hops", [])

    if not hops:
        logger.warning("No hops to visualize.")
        return

    logger.info(f"Visualizing traceroute with {len(hops)} hops...")

    G = nx.DiGraph()
    labels = {}
    previous_ip = None

    for hop in hops:
        ip = hop['ip']
        rtt = hop['rtts']
        avg_rtt = None

        if isinstance(rtt, list) and all(isinstance(val, int) for val in rtt):
            avg_rtt = sum(rtt) / len(rtt)
        elif isinstance(rtt, list) and rtt != ["*", "*", "*"]:
            try:
                avg_rtt = sum(int(x) for x in rtt if isinstance(x, str) and x.isdigit()) / len(rtt)
            except:
                avg_rtt = None

        label = f"{hop['hop']}: {ip}\nRTT: {avg_rtt if avg_rtt else 'N/A'}"

        G.add_node(ip, label=label, rtt=rtt)
        labels[ip] = label

        if previous_ip and ip != "*":
            G.add_edge(previous_ip, ip)

        if ip != "*":
            previous_ip = ip

    try:
        plt.figure(figsize=(12, 6))
        pos = nx.spring_layout(G)

        node_colors = []
        for node in G.nodes(data=True):
            rtts = node[1].get('rtt', [])
            if isinstance(rtts, list) and rtts != ["*", "*", "*"]:
                try:
                    avg_rtt = sum(map(int, rtts)) / len(rtts)
                    color = 'red' if avg_rtt > 100 else 'green'
                except:
                    color = 'gray'
            else:
                color = 'gray'
            node_colors.append(color)

        nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors)
        nx.draw_networkx_labels(G, pos, labels)
        nx.draw_networkx_edges(G, pos, arrows=True)

        plt.title(f"Traceroute to {traceroute_data['target']}")
        plt.axis('off')
        plt.tight_layout()

        if filename:
            plt.savefig(filename)  # Save the figure to the specified filename
            logger.info(f"Traceroute visualization saved to {filename}")
        else:
            plt.show()  # Display the figure if no filename is provided

        plt.close()  # Close the plot to free up memory
        logger.info("Traceroute visualization complete.")

    except Exception as e:
        logger.error(f"Error during visualization: {e}")

"""import networkx as nx
import matplotlib.pyplot as plt
from logger_utils import setup_logger

logger = setup_logger()

def visualize_traceroute(traceroute_data):
    hops = traceroute_data.get("hops", [])

    if not hops:
        logger.warning("No hops to visualize.")
        return

    logger.info(f"Visualizing traceroute with {len(hops)} hops...")

    G = nx.DiGraph()
    labels = {}
    previous_ip = None

    for hop in hops:
        ip = hop['ip']
        rtt = hop['rtts']
        avg_rtt = None

        if isinstance(rtt, list) and all(isinstance(val, int) for val in rtt):
            avg_rtt = sum(rtt) / len(rtt)
        elif isinstance(rtt, list) and rtt != ["*", "*", "*"]:
            try:
                avg_rtt = sum(int(x) for x in rtt if isinstance(x, str) and x.isdigit()) / len(rtt)
            except:
                avg_rtt = None

        label = f"{hop['hop']}: {ip}\nRTT: {avg_rtt if avg_rtt else 'N/A'}"

        G.add_node(ip, label=label, rtt=rtt)
        labels[ip] = label

        if previous_ip and ip != "*":
            G.add_edge(previous_ip, ip)

        if ip != "*":
            previous_ip = ip

    try:
        plt.figure(figsize=(12, 6))
        pos = nx.spring_layout(G)

        node_colors = []
        for node in G.nodes(data=True):
            rtts = node[1].get('rtt', [])
            if isinstance(rtts, list) and rtts != ["*", "*", "*"]:
                try:
                    avg_rtt = sum(map(int, rtts)) / len(rtts)
                    color = 'red' if avg_rtt > 100 else 'green'
                except:
                    color = 'gray'
            else:
                color = 'gray'
            node_colors.append(color)

        nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors)
        nx.draw_networkx_labels(G, pos, labels)
        nx.draw_networkx_edges(G, pos, arrows=True)

        plt.title(f"Traceroute to {traceroute_data['target']}")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        logger.info("Traceroute visualization complete.")
    except Exception as e:
        logger.error(f"Error during visualization: {e}")
        """