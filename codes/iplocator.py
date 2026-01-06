# Import necessary modules
import subprocess
import LocateIP
import socket
import requests
import whois

def Display_Menu():
    header = """
    __________________________
    |       IP Locater        |
    |       port scan         |
    |___________   ___________|
                \  \ 
                ^_ _^
                (o o)\_________
                (_ _)\         )/\/
                  U   ||----W||
                      ||     ||
    ### Tools:
        [1] localiser une adresse IP
        [2] scanner les port d'une adresse IP
        [3] ping
        [4] whois
        [5] quitter

    * taper <clear> pour supprimer les commandes precedente
    """
    print(header)


def option_1():
    """
    Option 1 --> IP Locater
    """
    LocateIP.locate_ip()
    Display_Menu()
    Home()

def option_2():
    """
     Option 2 --> port scanner
     """
    ip = input("Entrez l'adresse IP à scanner: ")
    start_port = 1
    end_port = 1024
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))  # Essaie de se connecter au port
        if result == 0:
            print(f"Port {port} est ouvert")
        sock.close()
def option_5():
    """
    Option 3 --> quitte le programme
    """

    quit()
def option_3():
    IP = input("entrer l'adresse IP a pingé")
    requests.get(IP)

def option_4():
    URL = input("entrez l'URL")
    print(whois.whois(URL))


def Home():
    """
    accueil du programme  selections des options
    """
    # options disponibles
    available_options = (1, 2,3,4,5)
    while True:
        try:
            selected_option = input("\nEnter your option\n>>> ")
            if selected_option == 'clear':
                subprocess.call('cls', shell=True)
                Display_Menu()
                continue
            else:
                selected_option = int(selected_option)
        except ValueError:
            print("entrez le numero d'une option")
            continue
        else:
            if selected_option not in available_options:
                print("l'option n'est pas disponible\nessayez en une autre")
                continue
            else:
                break

    if selected_option == 1:
        option_1()
    elif selected_option == 2:
        option_2()
    elif selected_option == 3:
        option_3()
    elif selected_option == 4:
        option_4()
    elif selected_option == 5:
        option_5()


# Run the program
def Start_Program():
    Display_Menu()
    Home()

