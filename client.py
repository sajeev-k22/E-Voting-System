import socket
import time

def start_client(server_ip, server_port):
    """ 
    Connects to the voting server, handles the voting process, and receives the results. 
    """ 
    try:
        # Establish a TCP connection to the server 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, server_port))
            print(f"Connected to voting server at {server_ip}:{server_port}\n")

            while True:
                # Receive data from the server 
                data = sock.recv(4096)
                if not data:
                    print("Server closed the connection.")
                    break

                # Decode and display the server message 
                message = data.decode()
                print(message, end='')  # end='' to avoid adding extra newline 

                # Determine if the server is prompting for input 
                if "Enter" in message:
                    # Get user input based on the server's prompt 
                    user_input = input()

                    # Measure latency
                    start_time = time.time()
                    sock.sendall(user_input.encode())
                    end_time = time.time()

                    latency = (end_time - start_time) * 1000  # Convert to milliseconds
                    print(f"Latency for sending input: {latency:.2f} ms")

                elif "The winner" in message or "No votes were recorded" in message:
                    # Final result received; close the connection 
                    print("\nVoting has ended. Disconnecting from the server.")
                    break

    except ConnectionRefusedError:
        print("Failed to connect to the server. Ensure the server is running and accessible.")
    except KeyboardInterrupt:
        print("\nClient shutdown initiated by user.")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        print("Disconnected from the server.")

if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # Replace with the server's IP address if different 
    SERVER_PORT = 23415           # Must match the server's VOTING_PORT 
    start_client(SERVER_IP, SERVER_PORT)