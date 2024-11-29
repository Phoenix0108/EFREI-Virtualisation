# TP Réseau : Configuration et Tests (TP2 - EFREI)

## Table des matières

1. [Introduction](#introduction)
2. [Configuration du routeur](#configuration-du-routeur)
3. [Configuration du switch](#configuration-du-node1)
4. [Serveur DHCP](#serveur-dhcp)
5. [Table ARP et Spoofing](#table-arp-et-spoofing)

---

## Configuration du routeur

### Interface 1 : Internet via DHCP (ens35)

- **Configuration :**

  ```bash
  ls
  - ifcfg-ens160 #Fichier de base présent servant pour ens35. Pourquoi ? David david GoodEnough et VMWARE

  vi ifcfg-ens160

  NAME=ens35
  DEVICE=ens35
  BOOTPROTO=dhcp
  ONBOOT=yes
  ```

- **Validation :**

  - `ping google.com` fonctionnel :

  ```bash
  PING google.com (142.250.178.142) 56(84) bytes of data.
  64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=1 ttl=127 time=35.4 ms
  64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=2 ttl=127 time=38.1 ms
  64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=3 ttl=127 time=35.2 ms
  ```

### Interface 2 : LAN avec IP statique (Routeur)

- **Configuration :**

  ```bash
  NAME=ens36
  DEVICE=ens36
  BOOTPROTO=static
  ONBOOT=yes
  IPADDR=10.2.1.254
  NETMASK=255.255.255.0
  ```

- **Validation :**

  - Adresse active :

    ```bash
    ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
        valid_lft forever preferred_lft forever
    2: ens35: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 00:0c:29:c8:f0:f1 brd ff:ff:ff:ff:ff:ff
        altname enp2s3
        inet 192.168.122.159/24 brd 192.168.122.255 scope global dynamic noprefixroute ens35
            valid_lft 2717sec preferred_lft 2717sec
        inet6 fe80::20c:29ff:fec8:f0f1/64 scope link noprefixroute
            valid_lft forever preferred_lft forever
    3: ens36: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 00:0c:29:c8:f0:fb brd ff:ff:ff:ff:ff:ff
        altname enp2s4
        inet 10.2.1.254/24 brd 10.2.1.255 scope global noprefixroute ens36
            valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fec8:f0fb/64 scope link
            valid_lft forever preferred_lft forever
    ```

  - Masquerading activé (COURS):

    ```bash
    sudo firewall-cmd --add-masquerade
    sudo firewall-cmd --add-masquerade --permanent
    ```

---

## Configuration du node1

### IP statique de node 1

- **Mise en place de l'ip statique :**

  ```bash
  ip 10.2.1.1/24

  Checking for duplicate address...
  PC1 : 10.2.1.1 255.255.255.0
  ```

- Vérification de l'ip depuis le routeur

  ```bash
    ping 10.2.1.1

    PING 10.2.1.1 (10.2.1.1) 56(84) bytes of data.
    64 bytes from 10.2.1.1: icmp_seq=1 ttl=64 time=2.35 ms
    64 bytes from 10.2.1.1: icmp_seq=2 ttl=64 time=2.53 ms
    64 bytes from 10.2.1.1: icmp_seq=3 ttl=64 time=1.62 ms
    ^C
    --- 10.2.1.1 ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2005ms
    rtt min/avg/max/mdev = 1.617/2.165/2.526/0.395 ms
  ```

- Mise en place du Gateway

  ```bash
    ip 10.2.1.1 10.2.1.254

    Checking for duplicate address...
    PC1 : 10.2.1.1 255.255.255.0 gateway 10.2.1.254
  ```

- Vérification

  ```bash
  show ip

  NAME        : PC1[1]
  IP/MASK     : 10.2.1.1/24
  GATEWAY     : 10.2.1.254
  DNS         :
  MAC         : 00:50:79:66:68:00
  LPORT       : 20004
  RHOST:PORT  : 127.0.0.1:20005
  MTU         : 1500

  PC1> ping 1.1.1.1

  84 bytes from 1.1.1.1 icmp_seq=1 ttl=126 time=41.015 ms
  84 bytes from 1.1.1.1 icmp_seq=2 ttl=126 time=54.154 ms
  ^C
  ```

- Traceroute

  ```bash
  trace 1.1.1.1
  trace to 1.1.1.1, 8 hops max, press Ctrl+C to stop
  1   10.2.1.254   2.252 ms  1.993 ms  2.183 ms
  2   192.168.122.1   3.285 ms  2.313 ms  2.997 ms
  3   192.168.72.2   3.632 ms  2.236 ms  2.333 ms
  ^C 4
  ```

## Vérification du switch

- **Table CAM :**

  ```bash
  show mac address-table
  Vlan    Mac Address       Type        Ports
  ----    -----------       --------    -----
  1       000c.29c8.f0fb    DYNAMIC     Et0/0
  1       0050.56c0.0003    DYNAMIC     Et0/0
  1       0050.7966.6800    DYNAMIC     Et0/1
  ```

---

## Serveur DHCP

### Configuration de l'interface (ens32)

- **Statique :**
  ```bash
  NAME=ens32
  DEVICE=ens32
  BOOTPROTO=static
  ONBOOT=yes
  IPADDR=10.2.1.253
  NETMASK=255.255.255.0
  ```

### Configuration DHCP

- **Fichier `/etc/dhcp/dhcpd.conf` :**
  ```bash
  default-lease-time 600;
  max-lease-time 7200;
  authoritative;
  subnet 10.2.1.0 netmask 255.255.255.0 {
      range dynamic-bootp 10.2.1.10 10.2.1.50;
      option broadcast-address 10.2.1.255;
      option routers 10.2.1.254;
      option domain-name-servers 1.1.1.1;
  }
  ```

### Validation

- **Lancement du service :**
  ```bash
  systemctl enable --now dhcpd
  ```
- **Test client DHCP (`node1.tp2.efrei`) :**

  - IP réinitialisé pour le test 'node1.tp2.efrei':

    ```
    show ip

    NAME        : VPCS[1]
    IP/MASK     : 0.0.0.0/0
    GATEWAY     : 0.0.0.0
    DNS         :
    MAC         : 00:50:79:66:68:00
    LPORT       : 20004
    RHOST:PORT  : 127.0.0.1:20005
    MTU         : 1500

    #DHCP

    dhcp
    DDORA IP 10.2.1.10/24 GW 10.2.1.254

    VPCS> show ip

    NAME        : VPCS[1]
    IP/MASK     : 10.2.1.10/24
    GATEWAY     : 10.2.1.254
    DNS         :
    DHCP SERVER : 10.2.1.253
    DHCP LEASE  : 594, 600/300/525
    MAC         : 00:50:79:66:68:00
    LPORT       : 20004
    RHOST:PORT  : 127.0.0.1:20005
    MTU         : 1500
    ```

  - Bonus : Gateway

  ```bash
    # create new
    #DNS
    option domain-name-servers 1.1.1.1;
    # default lease time
    default-lease-time 600;
    # max lease time
    max-lease-time 7200;
    # this DHCP server to be declared valid
    authoritative;
    # specify network address and subnetmask
    subnet 10.2.1.0 netmask 255.255.255.0 {
        # specify the range of lease IP address
        range dynamic-bootp 10.2.1.10 10.2.1.50;
        option broadcast-address 10.1.1.255;
        option routers 10.2.1.254;
    }
  ```

---

## Table ARP et Spoofing

### Table ARP

- **Table ARP du routeur (10.2.1.254) :**

  ```bash
  ip neigh show dev ens36

  10.2.1.1 lladdr 00:50:56:c0:00:03 REACHABLE
  10.2.1.253 lladdr 00:0c:29:d9:50:d7 STALE
  ```

### ARP Spoofing

- **Machine attaquante :**

  - IP : `10.2.1.12`.
  - Adresse mac : `00:0c:29:c1:9a:96`

- **Falsification de la table ARP (`node1.tp2.efrei`) :**

  ```bash
  arping -c 1 -S 10.2.1.254 -U -I ens33 10.2.1.11
  ```

- **Résultat (table ARP de victime):**
  ```bash
  arp
  00:0c:29:c1:9a:96  10.2.1.254 expires in 114 seconds
  ```
