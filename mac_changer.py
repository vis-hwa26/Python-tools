#!usr/bin/env pyhton3

import subprocess
import optparse
import re


def get_arguments():
    # assigning a variable for easy use
    parser = optparse.OptionParser()  # allows for giving arguments...

    # for adding options/different help commands..
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (a, arguments) = parser.parse_args()  # interface = options.interface | new_mac = options.new_mac
    if not a.interface:
        parser.error("[-] Please specify an interface, Use --help for more info")
    elif not a.new_mac:
        parser.error("[-] Please specify a new mac, Use --help for more info")
    return a


def change_mac(a, b):
    print("[+] Changing MAC address for " + a + " to " + b)

    subprocess.call(["ifconfig", a, "down"])
    subprocess.call(["ifconfig", a, "hw", "ether", b])
    subprocess.call(["ifconfig", a, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_add_search_result:
        return mac_add_search_result.group(0)
    else:
        print("\n" + "[-] Could not read MAC address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current Mac = " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address successfully changed to " + current_mac)
else:
    print("[-] Mac address failed to change.")
