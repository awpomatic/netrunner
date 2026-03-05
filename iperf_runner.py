from __future__ import annotations
import paramiko
import subprocess
import json
from typing import Any, Dict, Optional
import time
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
    iperf_check = subprocess.run(["iperf3", "--version"])
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
            server_launch = subprocess.run(["iperf3", "-s", "-D"])
            print(">>>>>>>>>>>>>>>>>>>>>>> Server online, initializing testcase >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(lucy_ASCII)
    else:
        print("Iperf does not exist!")
        print("Please exit and install Iperf3")


def tcp_runner(serverIP, client_ip, client_user):
    server_start()
    print("Server IP: " , serverIP, "\n", "Client IP: " ,  client_ip, "\n" , "Client User: ", client_user)
    ssh = ssh_connect(client_ip, client_user)

    _ , which_out, _ = ssh.exec_command("which iperf3")
    iperf_path = which_out.read().decode().strip()
    tcp_cmd = f"{iperf_path} -c {serverIP} -t 10 -J"
    stdin, stdout, stderr = ssh.exec_command(tcp_cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    if error:
        print("Error:", error)
    else:
        print(output)
    
def udp_runner(serverIP, client_ip, client_user):
    server_start()
    print("Server IP: " , serverIP, "\n", "Client IP: " ,  client_ip, "\n" , "Client User: ", client_user)
    ssh = ssh_connect(client_ip, client_user)

    _ , which_out, _ = ssh.exec_command("which iperf3")
    iperf_path = which_out.read().decode().strip()
    udp_cmd = f"{iperf_path} -c {serverIP} -u -t 10 -J"
    stdin, stdout, stderr = ssh.exec_command(udp_cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    if error:
        print("Error:", error)
    else:
        print(output)


def ssh_connect(client_ip, client_user):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    password = input("Please enter the password for the client device: ")
    ssh.connect(client_ip, username=client_user, password=password)
    return ssh
    










