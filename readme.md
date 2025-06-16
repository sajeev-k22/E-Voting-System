
🗳️ E-Voting System

This project is a simulation of an Electronic Voting System using a TCP-based client-server architecture with Python and MySQL. It validates voters, records their votes, and measures network performance including latency and round-trip time (RTT). Network loss can be simulated using Linux's `tcconfig`.

----------------------------------------
📁 Project Structure

E-Voting-System/

├── client.py                     # TCP client that allows a user to vote

├── server.py                     # Performance testing client to simulate vote submission

├── database.txt                  # SQL script to create and populate voting database

├── performance_metric_command.txt  # Network emulation commands using tcconfig

├── voting_performance_metrics.csv # Output CSV storing latency & RTT (auto-generated)

----------------------------------------
🚀 Features

- 🔒 Voter Authentication using Aadhar number and Date of Birth
- 🗳️ Vote Casting via terminal interface
- 📉 Performance Monitoring (latency and RTT for each vote)
- 📊 CSV Logging of vote performance metrics
- 🧪 Network Simulation using artificial packet loss (Linux-only)
- 🔁 Auto-retry and periodic vote simulations from server-side script

----------------------------------------
🧰 Setup Instructions

1. Clone the Repository
    git clone https://github.com/sajeev-k22/E-Voting-System.git
    cd E-Voting-System

2. MySQL Database Setup
    Run `database.txt` in MySQL to create tables and insert sample data:
    SOURCE path/to/database.txt;

3. Python Dependencies
    pip install tcconfig

4. Network Interface Simulation (Optional, Linux only)
    sudo tcset enp0s3 --loss 1%
    tcshow enp0s3  # Confirm settings
    sudo tcdel enp0s3 --all  # Reset settings

----------------------------------------
🧠 Networking Concepts Used

1. 🔗 TCP (Transmission Control Protocol)
    - Used for all communication between client and server
    - Reliable, ordered delivery of votes

2. 📶 UDP (User Datagram Protocol)
    - Not used due to lack of reliability, which is essential for voting systems

3. 📉 RTT & Latency Monitoring
    - Server simulates voting clients and logs network performance metrics

4. 🛜 Port Communication
    - Server listens on TCP port 12345

----------------------------------------
▶️ Running the System

Start the Server-Side Voting Simulator (Performance Logger)
    python3 server.py

Start the Voting Client
    python3 client.py

----------------------------------------
📊 Output Example

voting_performance_metrics.csv:
    timestamp,operation,latency,rtt
    2025-06-03 14:02:10,Submit Vote,1.1532,0.3872

----------------------------------------
🛠️ Future Improvements

- 🔐 SSL encryption
- 👨‍💼 Admin dashboard
- 🌐 Web interface
- 📱 Mobile app
- ✅ OTP verification

----------------------------------------
👨‍💻 Author

- Sajeev Kaleeswaran
- Email: sajeevkaleeswaran@gmail.com
- GitHub: github.com/sajeev-k22


