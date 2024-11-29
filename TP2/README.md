# TP Réseau : Configuration et Tests (TP2 - EFREI)

## Table des matières

1. [Introduction](#introduction)
2. [Configuration du routeur](#configuration-du-routeur)
3. [Configuration du switch](#configuration-du-switch)
4. [Serveur DHCP](#serveur-dhcp)
5. [Table ARP et Spoofing](#table-arp-et-spoofing)
6. [Prochaines étapes](#prochaines-étapes)

---

## Introduction

Ce document décrit la mise en place et les tests d'un réseau local avec routage, DHCP, et sécurité ARP.  
Les objectifs principaux sont :

- Configurer un routeur pour permettre l'accès Internet et la communication locale.
- Configurer un serveur DHCP pour l'attribution automatique des adresses IP.
- Tester la connectivité réseau et la robustesse face aux attaques ARP spoofing.

---

## Configuration du routeur

### Interface 1 : Internet via DHCP (ens35)

- **Configuration :**
  ```bash
  NAME=ens35
  DEVICE=ens35
  BOOTPROTO=dhcp
  ONBOOT=yes
  ```

````

- **Validation :**
  - `ping google.com` fonctionnel :
    ```
    PING google.com (142.250.178.142) 56(84) bytes of data.
    64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=1 ttl=127 time=35.4 ms
    ```

### Interface 2 : LAN avec IP statique (ens36)

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
    3: ens36: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 10.2.1.254/24 ...
    ```
  - Masquerading activé :
    ```bash
    sudo firewall-cmd --add-masquerade
    sudo firewall-cmd --add-masquerade --permanent
    ```

---

## Configuration du switch

- **Table CAM :**
  ```
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
      option broadcast-address 10.1.1.255;
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
  - IP obtenue dynamiquement :
    ```
    IP/MASK: 10.2.1.10/24
    GATEWAY: 10.2.1.254
    DHCP SERVER: 10.2.1.253
    ```
  - Accès Internet validé : `ping 1.1.1.1`.

---

## Table ARP et Spoofing

### Table ARP

- **Table ARP du routeur (ens36) :**
  ```bash
  ip neigh show dev ens36
  10.2.1.1 lladdr 00:50:56:c0:00:03 REACHABLE
  10.2.1.253 lladdr 00:0c:29:d9:50:d7 STALE
  ```

### ARP Spoofing

- **Machine attaquante :**
  - IP : `10.2.1.12`.
- **Falsification de la table ARP (`node1.tp2.efrei`) :**
  ```bash
  arping -c 1 -S 10.2.1.254 -U -I ens33 10.2.1.11
  ```
- **Résultat :**
  ```bash
  arp
  00:0c:29:c1:9a:96  10.2.1.254 expires in 114 seconds
  ```

---
````
