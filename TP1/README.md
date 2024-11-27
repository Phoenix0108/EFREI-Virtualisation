# TP Réseau : Mise en place et Configuration de Réseaux avec GNS3 et VirtualBox

## Sommaire
1. [I. Most Simple LAN](#i-most-simple-lan)
   - Objectifs
   - Étapes
2. [II. Ajout d'un Switch](#ii-ajout-dun-switch)
   - Objectifs
   - Étapes
3. [III. Serveur DHCP](#iii-serveur-dhcp)
   - 1. Configuration du Serveur DHCP Légitime
   - 2. DHCP Spoofing (Attaque DHCP)

---

## I. Most Simple LAN

**Objectifs** :

1. Monter la topologie dans GNS3 avec deux machines connectées par un câble.
2. Définir des adresses IP statiques sur les machines.
3. Vérifier la communication avec un `ping` entre les deux machines.
4. Visualiser le trafic avec Wireshark.
5. Effectuer un échange ARP.

### Étapes :

1. **Déterminer l'adresse MAC de vos deux machines** :
   - Depuis le terminal de chaque machine, exécutez la commande suivante :
     ```bash
     show ip
     ```
   - Réponse de la commande sur la machine 1 :
     ```bash
     NAME        : PC1[1]
     IP/MASK     : 10.1.1.1/24
     GATEWAY     : 0.0.0.0
     DNS         :
     MAC         : 00:50:79:66:68:03
     LPORT       : 20018
     RHOST:PORT  : 127.0.0.1:20019
     MTU         : 1500
     ```

2. **Définir une IP statique sur chaque machine** :
   - Commande pour `node1.tp1.efrei` :
     ```bash
     ip 10.1.1.1/24
     ```
   - Vérification pour `node1.tp1.efrei` :
     ```bash
     show ip

     NAME        : PC1[1]
     IP/MASK     : 10.1.1.1/24
     GATEWAY     : 0.0.0.0
     DNS         :
     MAC         : 00:50:79:66:68:03
     LPORT       : 20018
     RHOST:PORT  : 127.0.0.1:20019
     MTU         : 1500
     ```

3. **Effectuer un ping d'une machine à l'autre** :
   - Depuis `node1.tp1.efrei` :
     ```bash
     ping 10.1.1.2
     ```
   - Réponse :
     ```bash
     ping 10.1.1.2

     84 bytes from 10.1.1.2 icmp_seq=1 ttl=64 time=0.732 ms
     84 bytes from 10.1.1.2 icmp_seq=2 ttl=64 time=0.816 ms
     84 bytes from 10.1.1.2 icmp_seq=3 ttl=64 time=0.705 ms
     84 bytes from 10.1.1.2 icmp_seq=4 ttl=64 time=0.355 ms
     84 bytes from 10.1.1.2 icmp_seq=5 ttl=64 time=0.438 ms
     ```

4. **Wireshark** :
   - Capturez le trafic sous le nom "capturePing".
   - Protocole utilisé : ICMP

5. **Vérifier l'échange ARP** :
   - Sur `node1.tp1.efrei`, effectuez un `ping` pour rafraîchir la table ARP :
     ```bash
     ping 10.1.1.2
     ```

   - Affichez ensuite la table ARP :
     ```bash
     arp
     ```

   - Sortie :
     ```bash
     00:50:79:66:68:04  10.1.1.2 expires in 116 seconds
     ```

---

## II. Ajout d'un Switch

**Objectifs** :

1. Ajouter un switch pour connecter plusieurs machines entre elles.
2. Configurer les adresses IP sur trois machines.
3. Effectuer des tests de communication avec `ping`.

### Étapes :

1. **Déterminer l'adresse MAC de vos trois machines** :
   - Exécutez la commande suivante sur chaque machine :
     ```bash
     show ip
     ```

2. **Définir une IP statique sur chaque machine** :
   - Exemple pour `node1.tp1.efrei` :
     ```bash
     ip 10.1.1.1
     ```

   - Après redémarrage :
     ```bash
     show ip

     NAME        : PC1[1]
     IP/MASK     : 10.1.1.1/24
     GATEWAY     : 0.0.0.0
     DNS         :
     MAC         : 00:50:79:66:68:03
     LPORT       : 20018
     RHOST:PORT  : 127.0.0.1:20019
     MTU         : 1500
     ```

3. **Effectuer des pings entre les machines** :
   - Testez les connexions depuis `node1.tp1.efrei` :
     ```bash
     ping 10.1.1.2

     84 bytes from 10.1.1.2 icmp_seq=1 ttl=64 time=0.595 ms
     84 bytes from 10.1.1.2 icmp_seq=2 ttl=64 time=1.380 ms
     ^C
     ping 10.1.1.3

     84 bytes from 10.1.1.3 icmp_seq=1 ttl=64 time=1.956 ms
     84 bytes from 10.1.1.3 icmp_seq=2 ttl=64 time=0.773 ms
     ^C
     ```

   - Testez les connexions depuis `node2.tp1.efrei` :
     ```bash
     ping 10.1.1.3

     84 bytes from 10.1.1.3 icmp_seq=1 ttl=64 time=1.956 ms
     84 bytes from 10.1.1.3 icmp_seq=2 ttl=64 time=0.773 ms
     ^C
     ```

---

## III. Serveur DHCP

### 1. Configuration du Serveur DHCP Légitime

**Objectifs** :

1. Installer et configurer un serveur DHCP sur une machine Linux.
2. Configurer le serveur pour attribuer des adresses IP dynamiques dans la plage 10.1.1.10 à 10.1.1.50.

### Étapes :

1. **Ajouter un accès Internet à la machine `dhcp.tp1.efrei`** :
   - Ajoutez une carte réseau NAT pour installer le serveur DHCP.
     ```bash
     sudo dnf install dhcp-server
     ```

2. **Installer et configurer le serveur DHCP** :
   - Configuration du serveur DHCP pour distribuer des adresses IP entre 10.1.1.10 et 10.1.1.50.

     ```bash
     # DHCP Server Configuration file.
     #   see /usr/share/doc/dhcp-server/dhcpd.conf.example
     #   see dhcpd.conf(5) man page
     #
     # create new
     # default lease time
     default-lease-time 600;
     # max lease time
     max-lease-time 7200;
     # this DHCP server to be declared valid
     authoritative;
     # specify network address and subnetmask
     subnet 10.1.1.0 netmask 255.255.255.0 {
         # specify the range of lease IP address
         range dynamic-bootp 10.1.1.10 10.1.1.50;
         option broadcast-address 10.1.1.255;
     }
     ```

3. **Récupérer une IP automatiquement depuis les 3 machines** :
   - Commande à exécuter sur chaque machine :
     ```bash
     ip dhcp
     ```

4. **Wireshark** :
   - Capturez l'échange DORA (Discovery, Offer, Request, Acknowledge) entre les clients et le serveur DHCP.
   - La capture sera trouvée sous le nom 'captureDHCP'.

### 2. DHCP Spoofing (Attaque DHCP)

**Objectifs** :

1. Configurer une machine attaquante avec `dnsmasq` pour se faire passer pour un serveur DHCP.
2. Tester le spoofing DHCP en coupant le serveur légitime.

### Étapes :

1. **Configurer `dnsmasq` comme serveur DHCP malveillant** :
   - Installez `dnsmasq` et configurez-le pour attribuer des IPs dans la plage 10.1.1.210 à 10.1.1.250.

   - Configuration de `dnsmasq` :
     ```bash
     # Désactiver le serveur DNS
     port=0

     # Activer le DHCP uniquement
     dhcp-range=10.1.1.210,10.1.1.250,255.255.255.0,12h

     # Adresse réseau à écouter
     interface=ens33
     ```

2. **Tester l'attaque** :
   - Désactivez le serveur DHCP légitime sur `dhcp.tp1.efrei` et vérifiez si les clients récupèrent des adresses IP via le serveur malveillant.

   - IP après la désactivation du serveur légitime :
     ```bash
     ip dhcp
     DDORA IP 10.1.1.248/24 GW 10.1.1.14
     ```

3. **Wireshark** :
   - Capturez la course entre les deux serveurs DHCP (légitime et malveillant).
   - La capture sera trouvée sous le nom 'race'.
