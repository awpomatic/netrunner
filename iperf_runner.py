from __future__ import annotations
import paramiko
import subprocess
import json
from typing import Any, Dict, Optional
import time


def server_start(serverIP, client_ip, client_user):
    print("Verifiying Iperf version...")
    time.sleep(2.0)
    iperf_check = subprocess.run(["iperf3", "--version"])
    returnCode = iperf_check.returncode
   
    if returnCode == 0:
        print("Iperf exists! Initializing server...")
        server_launch = subprocess.run(["iperf3", "-s", "-D"])
        time.sleep(2.0)
        server_check = subprocess.run(["lsof", "-i", ":5201"])
        server_check = server_check.returncode
        if server_check == 0:
            
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

            print(lucy_ASCII)
            print(">>>>>>>>>>>>>>>>>>>>>>>Server online, initializing testcase>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            
        
    
def tcp_runner(serverIP, client_ip, client_user):
    server_start(serverIP, client_ip, client_user)
    print("Server IP: " , serverIP, "\n", "Client IP: " ,  client_ip, "\n" , "Client User: ", client_user)
    tcp_cmd = f"iperf3 -c {serverIP} -t 10 -J"



#def udp_runner():






