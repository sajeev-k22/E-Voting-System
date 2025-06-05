import socket
import time
import datetime
import csv
import threading
import logging
import mysql.connector

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

VOTING_SERVER_ADDRESS = ("127.0.0.1", 23415)

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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(VOTING_SERVER_ADDRESS)
    server.listen(5)
    logging.info(f"Server started on {VOTING_SERVER_ADDRESS}")

    while True:
        client_socket, client_address = server.accept()
        logging.info(f"New connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def handle_client(client_socket):
    try:
        # Send Aadhar prompt
        client_socket.send("Enter your Aadhar number: ".encode())
        aadhar = client_socket.recv(1024).decode().strip()

        # Send DOB prompt
        client_socket.send("Enter your date of birth (YYYY-MM-DD): ".encode())
        dob = client_socket.recv(1024).decode().strip()

        # Send candidate choice prompt
        client_socket.send("Enter candidate ID (1-3): ".encode())
        choice = client_socket.recv(1024).decode().strip()

        # Here you would validate and process the vote
        # For now, just send a confirmation
        client_socket.send("Vote recorded successfully!\n".encode())

    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
        save_performance_data()