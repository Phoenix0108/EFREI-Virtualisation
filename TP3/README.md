# TP 3 : Un ptit LAN maîtrisé

## Partie 1 : Setup Initial

### Get pinged !!

- Ping du PC1 (Lan 1) vers PC2 (LAN 2) après la configuration de l'infra réseau :

```bash
PC1> ping 10.3.2.1

84 bytes from 10.3.2.1 icmp_seq=1 ttl=62 time=30.920 ms
84 bytes from 10.3.2.1 icmp_seq=2 ttl=62 time=31.328 ms
84 bytes from 10.3.2.1 icmp_seq=3 ttl=62 time=26.043 ms
84 bytes from 10.3.2.1 icmp_seq=4 ttl=62 time=31.180 ms
```

- Table ARP de PC1 :

```bash
PC1> arp

c4:01:06:96:00:10  10.3.1.254 expires in 117 seconds
```

Ip de la Gateway du LAN 1 (On cherche a contacter une ip extérieur au LAN)

- Affichage de la Mac du routeur 1 :

```bash
R1#show arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.3.12.1               -   c401.0696.0001  ARPA   FastEthernet0/1
Internet  10.3.12.2              42   c402.06b4.0000  ARPA   FastEthernet0/1
Internet  10.3.1.1               12   0050.7966.6800  ARPA   FastEthernet1/0
Internet  10.3.1.254              -   c401.0696.0010  ARPA   FastEthernet1/0

```

- Affichage de la Mac du routeur 2 :

```bash
R2#show ARP
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.3.12.1              40   c401.0696.0001  ARPA   FastEthernet0/0
Internet  10.3.12.2               -   c402.06b4.0000  ARPA   FastEthernet0/0
Internet  10.3.2.1               10   0050.7966.6802  ARPA   FastEthernet0/1
Internet  10.3.2.254              -   c402.06b4.0001  ARPA   FastEthernet0/1
```

### Internet c'est fait pour partager nan ?

#### Connection LAN 1

- Configuration du routeur 1 pour un accès a internet :

```
R1(config)#conf t
R1(config)#interface fastEthernet 0/0
R1(config-if)#ip address dhcp
R1(config-if)#no shut
R1(config)#exit
```

- Vérification de l'adressage ip :

```
R1#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            192.168.122.253 YES DHCP   up                    up
```

- Vérification accès a internet :

```
R1#ping 1.1.1.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 88/108/148 ms
```

- Configuration pour que les LAN accèdent a internet :

```
R1(config)#interface fastEthernet 0/0
R1(config-if)#ip nat outside
exit

R1(config)#interface fastEthernet 0/1
R1(config-if)#ip nat inside
exit

R1(config)#interface fastEthernet 1/0
R1(config-if)#ip nat inside
exit

R1(config)#access-list 1 permit any

R1(config)#ip nat inside source list 1 interface fastEthernet 0/0 overload
R1(config)#exit
```

- Résultat sur le Lan 1 (avec PC 1) :

```bash
PC1> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=126 time=42.379 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=126 time=34.311 ms
84 bytes from 1.1.1.1 icmp_seq=3 ttl=126 time=33.407 ms
84 bytes from 1.1.1.1 icmp_seq=4 ttl=126 time=33.322 ms
84 bytes from 1.1.1.1 icmp_seq=5 ttl=126 time=37.035 ms
```

#### Connection LAN 2

- Route par défaut sur le routeur 2 (Internet uniquement):

```
R2(config)#ip route 0.0.0.0 0.0.0.0 10.3.12.1
```

- Test :

```
R2#ping 1.1.1.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 88/124/160 ms
```

- Test sur le PC 3 (LAN 2) :

```
PC3> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=125 time=51.535 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=125 time=89.471 ms
84 bytes from 1.1.1.1 icmp_seq=3 ttl=125 time=45.294 ms
84 bytes from 1.1.1.1 icmp_seq=4 ttl=125 time=63.742 ms
84 bytes from 1.1.1.1 icmp_seq=5 ttl=125 time=46.429 ms
```

Well well well. Tout marche correctement. Passons a la partie 2 :

## Partie 2 : Router-on-a-stick

### Configuration et test du VLAN 10

- Configuration du switch 1 pour le vlan 10 (Tout les autres VLAN sauf le trunk suivent la même conf) :

```
IOU1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
IOU1(config)#vlan 10
IOU1(config-vlan)#name pc1 3
IOU1(config-vlan)#exit
```

- Configuration du port du pc 1 pour le VLAN 10 :

```
IOU1(config)#interface Ethernet0/2
IOU1(config-if)#switchport mode access
IOU1(config-if)#switchport access vlan 10
IOU1(config-if)#exit
```

- Configuration du trunk entre le switch 1 et le switch 2 :

```
IOU1(config)#interface Ethernet0/1
IOU1(config-if)#switchport trunk encapsulation dot1q
IOU1(config-if)#switchport mode trunk
IOU1(config-if)#switch
*Dec 17 13:54:48.672: %LINEPROTO-5-UPDOWN: Line protocol on Interface Ethernet0/1, changed state to down
*Dec 17 13:54:51.668: %LINEPROTO-5-UPDOWN: Line protocol on Interface Ethernet0/1, changed state to up
IOU1(config-if)#switchport trunk allowed vlan add 10,20,30
IOU1(config-if)#exit
```

Les mêmes commandes ont été entré sur le switch 2 en adaptant juste les ports.

- Ping time (Après adressage ip bien sur 🤓):

```
PC1> ping 10.3.1.2

84 bytes from 10.3.1.2 icmp_seq=1 ttl=64 time=2.322 ms
84 bytes from 10.3.1.2 icmp_seq=2 ttl=64 time=1.315 ms
84 bytes from 10.3.1.2 icmp_seq=3 ttl=64 time=2.160 ms
84 bytes from 10.3.1.2 icmp_seq=4 ttl=64 time=1.790 ms
84 bytes from 10.3.1.2 icmp_seq=5 ttl=64 time=1.885 ms
```

```
PC3> ping 10.3.1.1

84 bytes from 10.3.1.1 icmp_seq=1 ttl=64 time=9.483 ms
84 bytes from 10.3.1.1 icmp_seq=2 ttl=64 time=2.528 ms
84 bytes from 10.3.1.1 icmp_seq=3 ttl=64 time=2.460 ms
84 bytes from 10.3.1.1 icmp_seq=4 ttl=64 time=2.281 ms

```

Le client 1 peut ping le client 3 et le client 3 peut ping le client 1

### Configuration du routeur (tout les vlan peuvent se ping)

- Configuration du routeur (sous interface):

```
R1(config)#interface f1/0.20
R1(config-subif)#encapsulation dot1Q 20
R1(config-subif)#ip address 10.3.2.254 255.255.255.0
R1(config)#interface fastEthernet 1/0
R1(config-subif)#exit
```

- Résultat de la config :

```
R1#show ip int br
Interface                  IP-Address      OK? Method Status                Prot             ocol
FastEthernet0/0            192.168.1.129   YES DHCP   up                    up
FastEthernet0/1            unassigned      YES unset  administratively down down
FastEthernet1/0            unassigned      YES unset  up                    up
FastEthernet1/0.10         10.3.1.254      YES manual up                    up
FastEthernet1/0.20         10.3.2.254      YES manual up                    up
FastEthernet1/0.30         10.3.3.254      YES manual up                    up
FastEthernet2/0            unassigned      YES unset  administratively down down
FastEthernet3/0            unassigned      YES unset  administratively down down
NVI0                       unassigned      NO  unset  up                    up
```

- Ping VLAN 1 vers VLAN 2

```
PC1> show ip

NAME        : PC1[1]
IP/MASK     : 10.3.1.1/24
GATEWAY     : 10.3.1.254
DNS         :
MAC         : 00:50:79:66:68:03
LPORT       : 20021
RHOST:PORT  : 127.0.0.1:20022
MTU         : 1500

PC1> ping 10.3.2.1

84 bytes from 10.3.2.1 icmp_seq=1 ttl=63 time=22.899 ms
84 bytes from 10.3.2.1 icmp_seq=2 ttl=63 time=25.872 ms
84 bytes from 10.3.2.1 icmp_seq=3 ttl=63 time=26.017 ms
84 bytes from 10.3.2.1 icmp_seq=4 ttl=63 time=26.208 ms

```

- Ping VLAN 2 ver VLAN 1 :

```

PC2> show ip

NAME        : PC2[1]
IP/MASK     : 10.3.2.1/24
GATEWAY     : 10.3.2.254
DNS         :
MAC         : 00:50:79:66:68:01
LPORT       : 20023
RHOST:PORT  : 127.0.0.1:20024
MTU         : 1500

PC2> ping 10.3.1.1

84 bytes from 10.3.1.1 icmp_seq=1 ttl=63 time=30.951 ms
84 bytes from 10.3.1.1 icmp_seq=2 ttl=63 time=17.939 ms
84 bytes from 10.3.1.1 icmp_seq=3 ttl=63 time=20.940 ms
84 bytes from 10.3.1.1 icmp_seq=4 ttl=63 time=16.375 ms
```

### Bienvenue sur internet

- Ping du routeur vers Internet :

```
R1#ping 1.1.1.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 20/47/92 ms

```

- Ping du pc 1 vers internet :

```
PC1> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=127 time=52.121 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=127 time=38.542 ms
```

- Ping du pc 2 vers internet :

```
PC2> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=127 time=54.137 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=127 time=45.265 ms
84 bytes from 1.1.1.1 icmp_seq=3 ttl=127 time=41.543 ms
84 bytes from 1.1.1.1 icmp_seq=4 ttl=127 time=46.316 ms
84 bytes from 1.1.1.1 icmp_seq=5 ttl=127 time=41.746 ms
```

### Partie 3 : Services dans le LAN

### DHCP (I WILL EXPLODE IF I HAVE TO DO THIS ONE MORE TIME LMAO)
