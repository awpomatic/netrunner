from __future__ import annotations
import paramiko
import subprocess
import json
from typing import Any, Dict, Optional
import time
import parser
import writer
import shutil
IPERF3_PATH = shutil.which("iperf3") or "/opt/homebrew/bin/iperf3"
lucy_ASCII = r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠄⠒⠒⠐⠒⠢⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠊⠙⣈⣔⣂⠀⠀⠀⠀⠀⠙⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠜⠀⠀⡾⡁⢠⢣⠀⠀⠀⠀⢀⠀⠀⠣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡌⢠⠀⢸⠋⠉⢸⡄⠀⡄⠀⠀⢩⡄⠀⢨⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⡆⠀⡇⠀⠀⣈⢧⠀⣧⠀⠀⢸⡇⠀⢸⠾⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠃⢀⡇⠀⠠⢤⣴⣽⡼⠢⠼⣦⣤⣼⢿⠀⠀⡸⢣⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⠀⢸⢇⠀⠲⣶⣒⣟⡜⠀⠀⣙⣿⣹⣿⠁⠀⡇⡟⡞⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⡇⢸⢸⡰⡇⠀⠉⠁⠀⠀⠀⠀⠉⠉⢸⠀⠀⡇⠁⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢇⢸⢸⣧⣶⡀⠀⠀⠀⠒⠂⠀⠀⠀⣌⠀⠀⣷⡀⣦⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣼⢾⡼⠏⡟⢗⣄⠀⠉⠛⠋⠀⢀⡴⡏⠀⢰⣿⣧⡟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠉⣦⡇⠸⢛⠿⣦⣀⣠⣴⠝⢻⠁⠀⡌⡷⠻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⣛⠇⠀⡀⠀⢸⠀⠀⡇⠀⡌⠀⠰⠑⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠤⢤⣤⣔⠛⡙⡍⠀⡔⡏⠀⠀⢻⢢⠁⢠⣧⢄⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡔⠊⠁⠀⠀⡠⠤⠤⠀⠀⢨⠇⠐⠠⢧⡉⢃⡰⢉⡌⢀⡿⠣⡅⠙⠒⠂⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⠀⠀⠀⠀⠀⠣⡀⠀⠀⡰⠉⠳⣄⠀⠀⠈⢇⡰⢩⢁⢾⣀⡤⠟⡉⠐⠒⠀⡤⠈⠑⢆⠀⠀⠀⠀⠀
⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⡇⢀⠞⠀⠀⢠⠱⠀⠀⠀⢨⡅⡌⡎⣸⠇⠀⠀⠘⡄⠀⡔⠁⠀⠀⠸⠀⠀⠀⠀⠀
⠠⠤⠀⡇⠀⠀⠀⠀⢀⠎⡠⠃⠀⠀⢀⣆⠃⠀⠀⢀⣾⣷⡇⢃⢻⡼⡄⠀⠀⠘⠄⢆⠀⠀⠀⠀⠂⠤⠤⠀⣀
⢫⠐⠒⠓⠀⠤⠄⠀⣸⣜⣡⠴⠖⠋⠉⠀⠀⠀⠱⠈⢎⡝⢨⠺⣼⠯⡙⠒⠦⣄⣈⢆⣎⣀⣀⠀⠤⠤⠄⠒⠍
⠀⠣⡀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠐⠒⠒⠠⠄⠀⡇⠀⠀⡆⣠⠌⠁⠒⠒⠒⠈⠉⠉⠀⠀⠀⠀⠀⠀⢠⠊⠀
⠀⠀⠑⠰⠀⠠⠤⠄⣀⣀⡀⠀⠀⠀⠀⠀⢰⠀⠀⡇⠀⡀⡇⡏⠀⠀⠀⠀⠀⣀⣀⠀⡤⠤⠄⠀⢀⠐⠁⠀⠀
⠀⠀⠀⡆⠀⠀⢀⠔⢹⠀⠈⠉⠁⠒⠂⠤⠼⡆⡰⠀⠀⡇⠰⡑⠄⠤⠒⠉⠁⠀⠀⢰⡀⠀⠀⠀⠸⠀⠀⠀⠀
⠀⠀⢠⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⢠⠀⠀⢠⠙⠁⠀⠀⠇⠀⢰⠀⠀⠀⠀⠀⠀⠀⠘⠱⠀⠀⠀⠀⡆⠀⠀⠀
⠀⠀⢸⠀⠀⠀⢀⠀⠀⢇⠀⠀⠀⠘⡄⠀⠘⠀⠀⠀⠀⢀⠀⠈⠀⠀⠀⠀⠀⠀⠀⡇⠀⢣⠀⠀⡠⠃⠀⠀⠀
⠀⠀⠀⢣⠀⠀⠎⠀⠀⠀⣷⡄⠀⠀⠇⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⡀⠀⠀⢀⠼⠀⠀⠀⢢⡔⠁⠀⠀⠀⠀
⠀⠀⠀⠀⢃⡌⠀⠀⠀⠀⠇⡎⠀⠀⢠⠀⠀⡾⠀⠀⠀⢸⠀⠤⠀⠀⡇⠀⢀⢤⠂⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⢀⠀⢏⠁⠚⢄⡀⡇⠀⠀⠀⢸⠀⠀⠀⢀⠗⠊⠀⢸⠀⠀⠀⠀⠀⡘⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢆⠀⠀⠀⠀⠀⢸⠀⠈⡄⠀⠀⠈⠃⠀⠀⠀⠈⠀⠀⠒⠁⠀⠀⠀⠿⡀⠀⠀⠀⠰⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⡸⠀⢠⠛⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⢡⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡆⠀⠀⠀⠀⢠⢣⠀⢇⠀⠘⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠐⠁⢀⠜⠀⠀⠀⠀⠀⢃⠀⠀⠀⠀
⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢸⠀⠀⠑⢄⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀⠀⠀⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

⠀"""


def server_start():
    print("Verifiying Iperf version...")
    time.sleep(2.0)
    iperf_check = subprocess.run([IPERF3_PATH, "-s", "-D"])

    returnCode = iperf_check.returncode
   
    if returnCode == 0:

        print("Iperf exists! Initializing server...")
        time.sleep(2.0)
        server_check = subprocess.run(["lsof", "-i", ":5201"])
        serverReturn = server_check.returncode
        if serverReturn == 0:
            time.sleep(2.0)
            print(">>>>>>>>>>>>>>>>>>>>>>> Server online, initializing testcase >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(lucy_ASCII)
        else:
            time.sleep(2.0)
            server_launch = subprocess.run([IPERF3_PATH, "-s", "-D"])

            print(">>>>>>>>>>>>>>>>>>>>>>> Server online, initializing testcase >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(lucy_ASCII)
    else:
        print("Iperf does not exist!")
        print("Please exit and install Iperf3")


def _find_remote_iperf3(ssh):
    _, out, _ = ssh.exec_command("command -v iperf3")
    path = out.read().decode().strip()
    if out.channel.recv_exit_status() == 0 and path:
        return path
    for candidate in ["/usr/bin/iperf3", "/usr/local/bin/iperf3", "/opt/homebrew/bin/iperf3", "/snap/bin/iperf3"]:
        _, out, _ = ssh.exec_command(f"test -x {candidate} && echo {candidate}")
        result = out.read().decode().strip()
        if out.channel.recv_exit_status() == 0 and result:
            return result
    return None


def tcp_runner(serverIP, client_ip, client_user, password):
    server_start()
    print("Server IP: " , serverIP, "\n", "Client IP: " ,  client_ip, "\n" , "Client User: ", client_user)
    ssh = ssh_connect(client_ip, client_user, password)

    iperf_path = _find_remote_iperf3(ssh)
    if not iperf_path:
        print("Error: iperf3 not found on the remote machine. Please install it first.")
        ssh.close()
        return
    tcp_cmd = f"{iperf_path} -c {serverIP} -t 10 -J"
    stdin, stdout, stderr = ssh.exec_command(tcp_cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    if error:
        print("Error:", error)
    else:
        print(output)
        results = parser.parse_tcp(output)
        writer.write_results(results, "TCP")

    
def udp_runner(serverIP, client_ip, client_user, password):
    server_start()
    print("Server IP: " , serverIP, "\n", "Client IP: " ,  client_ip, "\n" , "Client User: ", client_user)
    ssh = ssh_connect(client_ip, client_user, password)

    iperf_path = _find_remote_iperf3(ssh)
    if not iperf_path:
        print("Error: iperf3 not found on the remote machine. Please install it first.")
        ssh.close()
        return
    udp_cmd = f"{iperf_path} -c {serverIP} -u -t 10 -J"
    stdin, stdout, stderr = ssh.exec_command(udp_cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    if error:
        print("Error:", error)
    else:
        print(output)
        results = parser.parse_udp(output)
        writer.write_results(results, "UDP")


def ssh_connect(client_ip, client_user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(client_ip, username=client_user, password=password)
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {client_user}@{client_ip}. Check your username and password.")
        raise SystemExit(1)
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f"Could not connect to {client_ip}. Is the host reachable and is SSH running?")
        raise SystemExit(1)
    return ssh
    










