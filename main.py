import ipaddress
import paramiko
import subprocess
import iperf_runner
import time
import os
import random
import parser
import writer


def scramble_line(line):
    chars = '█░▓▒╳◈⚡#@%&'
    return ''.join(random.choice(chars) if c != ' ' else ' ' for c in line)



def animate_ascii(art):
    lines = art.split('\n')

    # scramble intro - each line decodes from random chars into real art
    for i, line in enumerate(lines):
        for _ in range(2):
            scrambled = scramble_line(line)
            print(f"\033[91m{scrambled}\033[0m")
            time.sleep(0.01)
            print('\033[1A\033[2K', end='')  # move up and clear line
        print(f"\033[31m{line}\033[0m")

    # static burst - flash random block characters over the whole art
    for _ in range(3):
        os.system('clear')
        static = '\n'.join(scramble_line(line) for line in lines)
        print(f"\033[91m{static}\033[0m")
        time.sleep(0.08)
    os.system('clear')
    print(f"\033[31m{art}\033[0m")
    time.sleep(0.3)

    # glitch effect - randomly shift lines briefly
    for _ in range(6):
        time.sleep(0.4)
        os.system('clear')
        glitch_line = random.randint(0, len(lines) - 1)
        glitch_shift = random.choice([-2, -1, 1, 2])
        colored_lines = []
        for i, line in enumerate(lines):
            if i == glitch_line:
                if glitch_shift > 0:
                    colored_lines.append(f"\033[91m{' ' * glitch_shift + line}\033[0m")
                else:
                    colored_lines.append(f"\033[91m{line[abs(glitch_shift):]}\033[0m")
            else:
                colored_lines.append(f"\033[31m{line}\033[0m")
        print('\n'.join(colored_lines))

    # scanline pulse - dim the whole art then bring it back
    for _ in range(3):
        # dim
        time.sleep(0.15)
        os.system('clear')
        print(f"\033[2m\033[31m{art}\033[0m")
        # bright
        time.sleep(0.15)
        os.system('clear')
        print(f"\033[1m\033[91m{art}\033[0m")

    # final clean red
    time.sleep(0.15)
    os.system('clear')
    print(f"\033[31m{art}\033[0m")



def server_check() -> str:
    interfaces = ["en0", "en1"]                 
    detected_ip = None

    for iface in interfaces:
        result = subprocess.run(
            ["ipconfig", "getifaddr", iface],
            capture_output=True,
            text=True
        )
        candidate = result.stdout.strip()
        if candidate:
            detected_ip = candidate
            break

    # If we detected something, validate it
    if detected_ip:
        try:
            ipaddress.ip_address(detected_ip)
            print(f"Detected server IP on {iface}: {detected_ip}")
            return detected_ip
        except ValueError:
            # Extremely rare, but don't trust blindly
            detected_ip = None

    # Fallback: manual input until valid
    while True:
        manual = input("Could not auto-detect IP. Enter server IP manually: ").strip()
        try:
            ipaddress.ip_address(manual)
            print(f"Using manual server IP: {manual}")
            return manual
        except ValueError:
            print("Invalid IP format. Try again.")


def client_check() -> tuple[str, str]:
    client_user = input("Please enter the username of the client: ").strip()
    while True:
        client_ip = input("Enter client IP (SSH target): ").strip()
        time.sleep(3.0)
        netrunner_ascii = r""" __   __     ______     ______   ______     __  __     __   __     __   __     ______     ______    
/\ "-.\ \   /\  ___\   /\__  _\ /\  == \   /\ \/\ \   /\ "-.\ \   /\ "-.\ \   /\  ___\   /\  == \   
\ \ \-.  \  \ \  __\   \/_/\ \/ \ \  __<   \ \ \_\ \  \ \ \-.  \  \ \ \-.  \  \ \  __\   \ \  __<   
 \ \_\\"\_\  \ \_____\    \ \_\  \ \_\ \_\  \ \_____\  \ \_\\"\_\  \ \_\\"\_\  \ \_____\  \ \_\ \_\ 
  \/_/ \/_/   \/_____/     \/_/   \/_/ /_/   \/_____/   \/_/ \/_/   \/_/ \/_/   \/_____/   \/_/ /_/ 
                                                                                                            """
        print (netrunner_ascii)
        try:
            ipaddress.ip_address(client_ip)
            return client_user, client_ip
        except ValueError:
            print("Invalid IP format. Example: 192.168.50.9")

def main():
    print('')
    print('')
    print('')
    print('')
    ascii_art = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⠿⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡟⠀⢀⡆⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠅⠀⠀⠀⠀⢀⡄⠀⠀⠀⣿⣿⣿⣗⣠⣾⡇⠀⠀⠀⠀⢠⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⢸⣆⠀⠀⢰⣿⣿⣿⣿⣿⣯⠀⢀⣴⠆⠀⠻⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⣷⠀⠀⠀⠀⠀⠀⢸⣿⠀⢀⣾⣿⣿⣿⣿⣿⡿⣥⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⡆⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢹⣿⠀⠀⠀⣴⠃⠀⣠⡆⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⣄⠀⠀⠀⠀⠈⣿⡇⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠘⠁⠀⠀⣰⣿⠀⢰⠟⠀⣤⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⠁⠀⢀⣰⣿⣿⡿⠆⠈⠀⣰⣷⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⣧⡜⠀⣠⣿⣿⣿⣿⡿⠋⣹⣿⣿⣿⠟⢸⣿⣦⣴⣿⣿⣿⡿⠁⠀⠀⣾⣿⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠀⠀⢹⣿⣧⠀⠀⠀⠀⡀⢀⣾⢀⣿⣿⣿⣾⣿⣿⣿⣿⠛⠁⢠⠿⠟⠉⠁⠀⢸⣹⣿⣿⠛⠻⣯⠁⠀⠀⣀⣿⠿⠁⠀⠀⠀⣆⢹
⠀⠀⠰⣄⠸⣷⡄⠀⢿⣟⠀⠀⠀⠀⣷⡀⣇⠀⣿⣿⠿⣿⠛⣿⠏⠀⠀⡄⠀⢀⣴⡾⠁⠀⣼⣿⡿⠏⠀⠐⣿⡄⠀⣰⠋⠀⠀⣺⠀⠀⠀⢹⣘
⠀⠀⠠⣽⣶⡿⠇⠀⠀⢉⠀⠶⠒⠀⠘⢷⣿⣥⠈⠿⠀⠘⢆⠘⠀⢠⣿⡁⠀⣾⣿⠃⠀⣸⢿⣿⣇⣀⠀⢀⣿⡇⠀⡘⠀⠀⠸⣿⠀⠀⠀⢸⠁
⠀⠀⠀⠘⠋⢀⠀⣄⠀⣆⠁⣾⣿⣧⠀⠘⣿⣿⣦⢸⣦⠀⠈⣤⣼⣿⣿⣿⣾⡿⠁⠀⠈⣠⣾⣿⣿⣿⣿⣿⣿⡇⢀⣧⠀⠲⣀⣿⡆⠀⠐⠀⠀
⠀⠀⠀⠀⡶⢠⣾⡿⠷⠿⢷⣿⣿⣿⠇⠀⠋⢹⣿⣶⣿⣷⣶⣿⣿⣿⠋⠉⣿⠃⠀⢀⣾⣿⣿⣿⣿⡿⠻⠙⠿⡇⠈⣿⠁⠀⣿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡀⠙⡁⠶⣿⡿⢒⣠⠀⡤⠀⢐⠀⠸⣿⣿⣿⣿⣿⡟⠉⢿⠀⢸⣿⡀⠀⢸⣿⣿⣿⠟⠁⠀⠀⠀⠀⢱⠀⠎⠠⠔⠁⠀⠀⠀⠀⠀⠀
⠀⠀⣶⠀⡇⢄⠘⠲⣦⠰⠟⠉⠒⠲⡄⠀⠁⢸⣿⠟⠁⢸⠟⢣⠀⠻⡀⠘⢿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠘⡆⠀⣶⠃⣰⡆⠀⠀⠀⠀⠀
⠂⠀⣿⣦⠈⠈⠛⢶⣦⠀⡸⡀⠀⠀⡸⠀⠀⠈⠁⠀⠰⠃⠀⢸⣄⠀⠘⠂⡀⢻⣿⡿⠟⠀⢤⠀⠀⠀⠀⠀⠀⢰⠗⢠⡯⢰⣿⠁⠀⠀⠀⠀⠀
⠀⣼⣿⡿⠁⠀⠈⢀⣄⠀⠷⣬⣑⡨⣴⡇⣴⠀⢀⣄⣠⣤⣴⣿⣾⣷⢄⡀⠀⠈⠀⠀⠈⠓⠋⠀⠀⠀⠀⢀⣼⠏⠀⣸⡇⢨⡏⠀⠀⠀⠀⠀⠀
⠀⢫⣿⡃⠀⢰⣿⣦⣅⡀⠛⠶⠶⠶⠌⠁⠀⠀⠀⠀⠉⠉⣿⣹⣿⠉⠙⣌⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡞⠁⠀⣰⢫⡇⠈⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠇⠘⠘⢿⣥⣀⠉⠛⣿⣷⣶⣿⣿⡟⢀⣴⠂⠀⠀⠀⠹⣿⣧⡀⠀⠙⢦⡀⠀⠀⢦⣄⣤⣨⣭⣤⣠⠴⠋⠀⠸⠁⠀⢦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣬⣙⡛⠓⠒⢒⢀⣤⠀⣄⠻⣿⣄⠀⠀⠀⢀⣿⣿⣽⣦⡀⠀⠀⠳⣄⡀⠀⠈⠛⠛⠛⠁⠀⡠⠞⠁⠀⠻⣦⡹⣦⡐⢄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⣻⠟⣛⣃⣸⣿⡇⣹⣿⡷⠀⣠⠟⢻⣿⢿⠛⠋⠃⡄⠀⠈⢿⣶⣶⠦⢶⡖⠆⢁⣄⠐⢿⣷⣄⠈⠻⣌⢻⣆⠡⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢋⣼⣿⣿⡿⠙⢁⣾⣿⡇⠀⠀⣠⣾⣿⠀⠀⠀⣴⠃⠀⣀⣀⡈⠉⠛⢷⣾⠀⠻⣿⣷⣄⠙⠛⣡⣄⡹⣧⠹⡇⢱
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠘⠗⣠⣌⠛⠀⠹⠿⠿⣇⠀⠀⠻⠿⠋⠀⠀⠋⠁⡔⠚⠉⣉⡋⠐⠀⠀⢟⠀⠀⠈⠻⣿⠇⣀⠈⠛⢛⣿⡗⢃⡌
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⢛⣴⣿⣿⣧⠰⣷⢰⡆⣶⢠⠀⠰⣦⣤⣤⣴⠶⠉⠀⢰⣾⣿⣿⣦⠈⠀⠀⠀⠀⠀⠀⠨⡘⢿⣿⣿⣿⣿⠇⡼⠀
⠀⠀⠀⠀⢀⣀⣤⠶⢟⣫⣴⣿⣿⣿⣿⠏⠰⣤⡤⠔⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⠀⠈⠻⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠈⠒⠦⠭⠭⠥⠚⠀⠀
⠀⠀⠴⠞⣛⣭⣴⣾⣿⣿⣿⣿⠿⠛⣡⢸⣷⣌⠓⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⣦⠐⣌⠻⢿⣿⣿⣷⣦⣬⣓⡒⠤⠤⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠤⣭⣭⣭⣭⣭⣭⣭⣭⠐⢶⡃⠉⠘⠿⠿⠈⡁⣠⣾⣿⣿⢿⣷⣶⣄⡙⠂⢾⣿⠀⠟⣡⣤⣍⡛⠻⢿⣿⣿⣿⡿⠶⢒⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠈⢿⣤⣀⣀⣦⠿⠛⠉⢁⡀⠀⢀⣀⡀⠙⠹⠿⣷⣦⣤⣞⣿⣿⠟⠀⠘⠓⠲⠶⠶⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠋⣡⡴⢁⣴⣿⣿⣦⣶⣿⣷⣄⠀⢶⣤⣭⠍⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⠿⠟⠻⠿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

    animate_ascii(ascii_art)
    print('Welcome to NETRUNNER!')
    serverIP = server_check()
    print("Your server:", serverIP)
    client_user, client_ip = client_check()
    import getpass
    password = getpass.getpass("Please enter the password for the client device: ")
    while True:

        print("\nSelect Test Type:")
        print("1: TCP")
        print("2: UDP")
        print("3: Exit")

        choice = input("Enter selection: ")

        if choice == "1":
            iperf_runner.tcp_runner(serverIP, client_ip, client_user, password)
            print("Running TCP")
        elif choice == "2":
            iperf_runner.udp_runner(serverIP, client_ip, client_user, password)
            print("Running UDP")
        elif choice == "3":
            print("Exiting, killing server...")
            time.sleep(2.0)
            serverKill = subprocess.run(["pkill", "iperf3"])
            
            print("See ya choom...")
            break
        else:
            print("Invalid entry")
            
if __name__ == "__main__":
    main()