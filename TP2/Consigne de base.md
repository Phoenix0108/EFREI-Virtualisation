# TP2 : Routage, DHCP et DNS

Objectifs de ce TP :

- comme toujours, on réutilise les trucs qu'on a vu auparavant
- on appréhende des nouveaux outils et/ou protocoles
  - ici ce sera la mise en place d'un routeur très basique
  - setup d'un serveur DHCP (ui encore) avec une petite option en plus
  - et setup d'un serveur DNS
- je veux vous familiariser avec les choses qu'on voit TOUT LE TEMPS en réseau, et vous faire monter ça vous-mêmes, dans un lab virtuel

On va encore tout faire avec Rocky Linux (ou l'OS de votre choix), toujours la même idée : les systèmes Linux sont des couteaux suisse qu'il est facile de manipuler.

![Dancin netadmin](img/sysadmin-hotline.gif)

# Sommaire

- [TP2 : Routage, DHCP et DNS](#tp2--routage-dhcp-et-dns)
- [Sommaire](#sommaire)
- [0. Setup](#0-setup)
- [I. Routage](#i-routage)
- [II. Serveur DHCP](#ii-serveur-dhcp)
- [III. ARP](#iii-arp)
  - [1. Les tables ARP](#1-les-tables-arp)
  - [2. ARP poisoning](#2-arp-poisoning)

# 0. Setup

➜ **Télécharge le ptit [IOU : un OS de switch Cisco.](https://labhub.eu.org/api/raw/?path=/UNETLAB%20I/addons/iol/bin/i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin)**

- vous n'utiliserez que ça comme comme switch à partir de ce TP

➜ **VM Rocky Linux** toujours pour les machines client/serveur

➜ **VPCS** pour les clients quand on a juste besoin d'une IP et faire des pings

# I. Routage

![Topo 1](./img/topo1.png)

➜ **Tableau d'adressage**

| Nom                | IP              |
| ------------------ | --------------- |
| `router.tp2.efrei` | `10.2.1.254/24` |
| `node1.tp2.efrei`  | `10.2.1.1/24`   |

➜ **Reproduisez la topologie dans votre GNS3**, quelques hints :

- il faudra indiquer à GNS que votre `router.tp2.efrei` a une carte réseau supplémentaire
- le NAT est disponible dans la catégorie "End Devices"
  - il va symboliser un accès internet

🌞 **Configuration de `router.tp2.efrei`**

- l'interface de `router.tp2.efrei` qui est branchée au NAT doit être configurée automatiquement _via_ DHCP, la magie de GNS :)
  - c'est indiqué dans le [mémo Rocky](../../memo/rocky_network.md) comment setup une interface pour qu'elle récup une IP en DHCP
  - une fois qu'elle a récupéré une IP, prouvez que vous avez un accès internet en une commande `ping`
- l'autre interface de `router.tp2.efrei` sera configurée statiquement
  - voir l'IP demandée dans le tableau d'adressage juste au dessus
- je veux un beau `ip a` une fois que tout est conf !

Aussi, on va demander à cette machine Rocky de ne pas jeter les paquets IPs qui ne lui sont pas destinés, **afin qu'elle puisse agir comme un routeur**.

Pour ça, deux commandes à exécuter sur `router.tp2.efrei` :

```bash
# Petite modif du firewall qui nous bloquerait sinon
[it4@router ~]$ sudo firewall-cmd --add-masquerade
success

# Et on tape aussi la même commande une deuxième fois, en ajoutant --permanent pour que ce soit persistent après un éventuel reboot
[it4@router ~]$ sudo firewall-cmd --add-masquerade --permanent
success
```

🌞 **Configuration de `node1.tp2.efrei`**

- configurer de façon statique son IP
  - voir l'IP demandée dans le tableau d'adressage juste au dessus
- prouvez avec une commande `ping` que `node1.tp2.efrei` peut joindre `router.tp2.efrei`
- ajoutez une route par défaut qui passe par `router.tp2.efrei`
- prouvez que vous avez un accès internet depuis `node1.tp2.efrei` désormais, avec une commande `ping`
- utilisez une commande `traceroute` pour prouver que vos paquets passent bien par `router.tp2.efrei` avant de sortir vers internet

➜ A la fin de cette section vous avez donc :

- un routeur, qui, grâce à du NAT, est connecté à Internet
- il est aussi connecté au LAN `10.2.1.0/24`
- les clients du LAN, comme `node1.tp2.efrei` ont eux aussi accès internet, en passant par `router.tp2.efrei` après l'ajout d'une route

🌞 **Afficher la CAM Table du switch**

- sur le switch IOU mis en place, affichez la CAM Table
- un switch apprend les adresses MAC de toutes les personnes qui envoient des messages
- la CAM table contient les infos de quelle MAC est branché sur quel port
- la commande c'est `show mac address-table` une fois connecté au terminal du switch

# II. Serveur DHCP

![Topo 2](./img/topo2.png)

➜ **Tableau d'adressage**

| Nom                | IP              |
| ------------------ | --------------- |
| `router.tp2.efrei` | `10.2.1.254/24` |
| `node1.tp2.efrei`  | `N/A`           |
| `dhcp.tp2.efrei`   | `10.2.1.253/24` |

🌞 **Install et conf du serveur DHCP** sur `dhcp.tp2.efrei`

- pour l'install du serveur, il faut un accès internet... il suffit d'ajouter là encore une route par défaut, qui passe par `router.tp2.efrei`
- référez-vous au [TP1](../1/README.md)
- cette fois, dans la conf, ajoutez une option DHCP pour donner au client l'adresse de la passerelle du réseau (c'est à dire l'adresse de `router.tp2.efrei`) en plus de leur proposer une IP libre

🌞 **Test du DHCP** sur `node1.tp2.efrei`

- enlevez toute config IP effectuée au préalable
- vous pouvez par exemple `sudo nmcli con del enp0s3` s'il s'agit de l'interface `enp0s3` pour supprimer la conf liée à `enp0s3`
- configurez l'interface pour qu'elle récupère une IP dynamique, c'est à dire avec DHCP
- vérifiez que :
  - l'IP obtenue est correcte
  - votre table de routage a bien été mise à jour automatiquement avec l'adresse de la passerelle en route par défaut (votre option DHCP a bien été reçue !)
  - vous pouvez immédiatement joindre internet

![DHCP](img/dhcp_server.png)

🌟 **BONUS**

- ajouter une autre ligne dans la conf du serveur DHCP pour qu'il donne aussi l'adresse d'un serveur DNS (utilisez `1.1.1.1` comme serveur DNS : c'est l'un des serveurs DNS de CloudFlare, un gros acteur du web)

🌞 **Wireshark it !**

- je veux une capture Wireshark qui contient l'échange DHCP DORA
- vous hébergerez la capture dans le dépôt Git avec le TP

> Si vous fouillez un peu dans l'échange DORA? vous pourrez voir les infos DHCP circuler : comme votre option DHCP qui a un champ dédié dans l'un des messages.

➜ A la fin de cette section vous avez donc :

- un serveur DHCP qui donne aux clients toutes les infos nécessaires pour avoir un accès internet automatique

# III. ARP

## 1. Les tables ARP

ARP est un protocole qui permet d'obtenir la MAC de quelqu'un, quand on connaît son IP.

On connaît toujours l'IP du correspondant avant de le joindre, c'est un prérequis. Quand vous tapez `ping 10.2.1.1`, vous connaissez l'IP, puisque vous venez de la taper :D

La machine va alors automatiquement effectuer un échange ARP sur le réseau, afin d'obtenir l'adresse MAC qui correspond à `10.2.1.1`.

Une fois l'info obtenue, l'info "telle IP correspond à telle MAC" est stockée dans la **table ARP**.

> Pour toutes les manips qui suivent, référez-vous au [mémo réseau Rocky](../../memo/rocky_network.md).

🌞 **Affichez la table ARP de `router.tp2.efrei`**

- vérifiez la présence des IP et MAC de `node1.tp2.efrei` et `dhcp.tp2.efrei`
- s'il manque l'une et/ou l'autre : go faire un `ping` : l'échange ARP sera effectuée automatiquement, et vous devriez voir l'IP et la MAC de la machine que vous avez ping dans la table ARP

🌞 **Capturez l'échange ARP avec Wireshark**

- je veux une capture de l'échange ARP livrée dans le dépôt Git
- l'échange ARP, c'est deux messages seulement : un ARP request et un ARP reply

## 2. ARP poisoning

**Insérer une machine attaquante dans la topologie. Un Kali linux, ou n'importe quel autre OS de votre choix.**

🌞 **Envoyer une trame ARP arbitraire**

- depuis la machine attaquante, envoyer un message à la victime (`node1.tp2.efrei`)
- en utilisant la commande `arping`
- écrivez des données arbitraires dans la table ARP de `node1.tp2.efrei`

🌞 **Mettre en place un ARP MITM**

- setup un MITM (man-in-the-middle) à l'aide d'ARP poisoning
- il faut se mettre entre `node1.tp2.efrei` et `router.tp2.efrei`
- donc il faut ARP spoof pour que :
  - `node1` pense que la MAC de `router` c'est la MAC de l'attaquant
  - `router` pense que la MAC de `node1` c'est la MAC de l'attaquant
  - ainsi, tous les messages échangés entre les deux, seront en réalité envoyés à l'attaquant
- utilisez la commande `arpspoof` pour faire ça
  - une seule commande suffit pour mettre en place toute l'attaque

> Il sera nécessaire d'activer l'IPv4 forwarding sur la machine attaquante. L'IPv4 forwarding permet à la machine attaquante d'accepter les paquets IP qui ne lui sont pas destinées (c'est à dire : agir comme un routeur).

🌞 **Capture Wireshark `arp_mitm.pcap`**

- la victime ping `1.1.1.1`
- la capture Wireshark est réalisée depuis la machine attaquante
- on doit voir les pings de la victime qui circulent par la machine attaquante

🌞 **Réaliser la même attaque avec Scapy**

- un ptit script Python qui met en palce exactement la même attaque
- l'intérêt est de commencer à utiliser Scapy avec une attaque que vous connaissez déjà (donc la seule barrière doit être l'apprentissage de la yntaxe Scapy)
- remettre le script `arp_mitm.py` dans le dépôt git de rendu

![ARP sniffed ?](img/arp_sniff.jpg)
