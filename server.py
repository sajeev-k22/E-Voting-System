import socket
import time
import datetime
import csv
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

VOTING_SERVER_ADDRESS = ("127.0.0.1", 12345)

performance_data = []  # Store performance data for each request

def log_performance(operation, start_time, end_time, rtt):
    latency = end_time - start_time
    data = {
        'timestamp': datetime.datetime.now(),
        'operation': operation,
        'latency': latency,
        'rtt': rtt
    }
    performance_data.append(data)
    logging.debug(f"Logged performance data: {data}")

def get_user_input(prompt):
    """Get input from the user based on the server's prompt."""
    return input(prompt).strip()

def measure_rtt(client, data_to_send):
    start_time = time.time()
    client.send(data_to_send.encode())
    client.recv(4096)  # Adjust buffer size if needed
    return time.time() - start_time

def handle_voting_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)  # Timeout to prevent infinite blocking
    try:
        client.connect(VOTING_SERVER_ADDRESS)
        logging.info("Connected to Voting Server")

        start_time = time.time()
        total_rtt = 0
        rtt_count = 0

        # Aadhar number prompt
        prompt = client.recv(1024).decode()  # Adjust buffer size if needed
        logging.debug("Received prompt for Aadhar number")
        aadhar_number = get_user_input(prompt)
        rtt = measure_rtt(client, aadhar_number)
        total_rtt += rtt
        rtt_count += 1

        # Date of Birth prompt
        prompt = client.recv(1024).decode()  # Adjust buffer size if needed
        logging.debug("Received prompt for Date of Birth")
        dob = get_user_input(prompt)
        rtt = measure_rtt(client, dob)
        total_rtt += rtt
        rtt_count += 1

        # Candidate choice prompt
        prompt = client.recv(1024).decode()  # Adjust buffer size if needed
        logging.debug("Received prompt for candidate choice")
        candidate_id = get_user_input(prompt)
        rtt = measure_rtt(client, candidate_id)
        total_rtt += rtt
        rtt_count += 1

        end_time = time.time()
        avg_rtt = total_rtt / rtt_count if rtt_count > 0 else 0
        log_performance("Voting Server - Submit Vote", start_time, end_time, avg_rtt)

    except socket.timeout:
        logging.error("Timeout occurred during communication with Voting Server")
    except Exception as e:
        logging.error(f"Error in handle_voting_server: {e}")
    finally:
        client.close()

def make_requests():
    while True:
        try:
            handle_voting_server()
            
            # Save after each cycle
            save_performance_data()
            
            # Sleep interval to simulate periodic requests
            time.sleep(60)
        
        except Exception as e:
            logging.error(f"Error in make_requests: {e}")
            time.sleep(10)  # Wait before retrying if there's an error

def save_performance_data():
    try:
        with open('voting_performance_metrics.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'operation', 'latency', 'rtt']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in performance_data:
                writer.writerow(data)
        logging.info(f"Saved {len(performance_data)} records to voting_performance_metrics.csv")
    except Exception as e:
        logging.error(f"Error saving performance data: {e}")

if name == "main":
    try:
        make_requests()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Saving final performance data...")
        save_performance_data()