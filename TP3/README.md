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

## Partie 2 : Partie II. Router-on-a-stick
