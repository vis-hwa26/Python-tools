#!/usr/bin/env python

import scapy.all as scapy
import optparse               # argparse


def get_ip():
    parser = optparse.OptionParser()            # argparse.ArgumentParser()
    parser.add_option("-t", "--target", dest="IP", help="Target ip address")             # add_argument
    (a, arguments) = parser.parse_args()                         # only options/a
    return a


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for i in answered_list:
        clients_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC ADDRESS\n--------------------------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_ip()
print_result(scan(options.IP))
