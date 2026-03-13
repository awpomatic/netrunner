# Netrunner

A network testing tool that SSHes into a client device and runs iperf3 TCP and UDP tests from your local machine. Results are saved to a CSV file after each test.

---

## Requirements

You need the following installed on **both** the server machine (your Mac) and the client machine (the device you are testing against).

### Server Machine (your Mac)

- Python 3.10 or higher
- iperf3
- pip packages: `paramiko`

### Client Machine (Linux/Mac)

- iperf3
- SSH server enabled and running

---

## Installation

### 1. Install iperf3 on your Mac (server)

```bash
brew install iperf3
```

If you don't have Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install iperf3 on the client (Linux)

```bash
sudo apt install iperf3
```

Verify it installed:
```bash
iperf3 --version
```

### 3. Enable SSH on the client (Linux)

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
```

The status should say `active (running)`.

### 4. Clone the repo on your Mac

```bash
git clone <your-repo-url>
cd netrunner
```

### 5. Create a virtual environment and install Python dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install paramiko
```

---

## Running the tool

Make sure you are in the `netrunner` directory with the virtual environment active:

```bash
source venv/bin/activate
python main.py
```

---

## What happens when you run it

1. An animated startup screen plays
2. The tool auto-detects your server IP (or asks you to enter it manually)
3. You enter the client username and IP address
4. You enter the client SSH password — **you only need to enter this once**
5. A menu appears:
   - `1` — Run a TCP test (10 seconds)
   - `2` — Run a UDP test (10 seconds)
   - `3` — Exit and kill the iperf3 server

After each test, results are appended to `results.csv` in the project folder.

---

## results.csv format

Each row is one test run:

| Test Type | Throughput | Jitter | Packet Loss |
|-----------|------------|--------|-------------|
| TCP | 94.23 Mbps | | |
| UDP | 91.10 Mbps | 0.31 ms | 0.02 % |

TCP rows have throughput only. UDP rows include throughput, jitter, and packet loss.

---

## Troubleshooting

**SSH connection refused or timed out**
- Make sure the client machine has SSH running: `sudo systemctl status ssh`
- Make sure you can ping the client: `ping <client-ip>`
- Make sure both machines are on the same network

**iperf3 not found on client**
- Run `iperf3 --version` on the client to confirm it is installed
- If not, run `sudo apt install iperf3`

**iperf3 not found on server (your Mac)**
- Run `iperf3 --version` in your terminal
- If not found, run `brew install iperf3`

**paramiko import error**
- Make sure your virtual environment is active: `source venv/bin/activate`
- Then run: `pip install paramiko`

**Port 5201 already in use**
- Kill any existing iperf3 server: `pkill iperf3`
- Then run the tool again
