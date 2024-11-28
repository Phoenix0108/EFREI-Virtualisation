# TP1 : Remise dans le bain

**Ce TP va servir d'introduction**, pour mieux apprendre à se connaître, et que vous mettiez la main sur des outils qu'on utilisera probablement tout le long du cours.

Le cours, justement, est intitulé "Virtualisation Réseau", **on va donc profiter de ce premier TP pour mettre en place nos outils de virtualisation**, et commencer à jouer avec.

## Sommaire

- [TP1 : Remise dans le bain](#tp1--remise-dans-le-bain)
  - [Sommaire](#sommaire)
  - [0. Setup](#0-setup)
- [I. Most simplest LAN](#i-most-simplest-lan)
- [II. Ajoutons un switch](#ii-ajoutons-un-switch)
- [III. Serveur DHCP](#iii-serveur-dhcp)
  - [1. Legit](#1-legit)
  - [2. DHCP spoofing](#2-dhcp-spoofing)
  - [3. BONUS : DHCP starvation](#3-bonus--dhcp-starvation)

## 0. Setup

➜ **Téléchargez de suite** :

- un outil pour **virtualiser des équipements réseau** et simuler des connexions réseau
  - on utilisera [**GNS3**](https://www.gns3.com/)
- un outil pour **gérer des VMs**
  - je vous recommande [**VirtualBox**](https://www.virtualbox.org/)
  - il faut qu'il soit compatible avec GNS3
- un outil de **sniffing réseau**
  - je vous recommande l'excellent [**Wireshark**](https://www.wireshark.org/) évidemment

Pour ce premier TP, on va commencer smooth, et on utilisera avec ces deux outils de virtu -GNS3 et VirtualBox- uniquement des systèmes Linux.

> *On utilisera souvent des OS Linux dans le cours, c'est pour nous un outil de choix : un outil robuste et éprouvé dans le milieu pro, qui est de plus ouvert et transparent dans son fonctionnement.*

➜ **Téléchargez aussi un OS Linux de votre choix** (un truc un peu classique, pas un truc de barbu perdu de préférence) :

- je vous recommande [Rocky Linux](https://rockylinux.org/), c'est un dérivé de RHEL
- mais vous pouvez préférer n'importe lequel avec vous êtes à l'aise : Debian, Ubuntu (beurk), autres.
- pas d'interface graphique nécessaire, habituez-vous à être économes avec les ressources : l'énergie ça pousse pas dans les arbres 🙃

➜ Une fois les outils téléchargés et prêts à être lancer, vous pouvez passer à la suite du TP :

- chaque partie correspond à une topologie à réaliser dans GNS3
- vous vous servirez de VPCS pour les clients ou de machines Linux
- installez l'OS de votre choix sur une nouvelle VM, et éteignez là. Vous pourrez la cloner à l'infini dès que vous avez besoin d'une machine pour un TP
- rappel : je veux un compte-rendu qui contient TOUTES les commandes réalisées

> ***N'hésitez pas à m'appeler, autant de fois que nécessaire, si une étape n'est pas claire, si vous comprenez mal quelque chose, ou pour toute question.***

# I. Most simplest LAN

![Topologie n°1](./img/topo1.png)

> *VM Linux ou VPCS, libre à vous !*

Un LAN (ou "Réseau Local" en français) c'est juste un réseau formé de plusieurs machines connectées physiquement entre elles.

Pour ça, chaque machine a besoin d'au moins une carte réseau, et on relie par des câbles les machines entre elles. (Merci captain obvious ?)

On va donc commencer au plus simple : deux machines connectées par un câble.

Les objectifs de cette partie :

- monter la topologie dans GNS3 *(drag'n'drop des machins et tirer des câbles dans GNS3)*
- définir des IPs sur les deux machines
- visualiser l'IP choisie, ainsi que l'adresse MAC prédeterminée
- vérifier que les deux machines peuvent communiquer en faisant un `ping`
- visualiser le `ping` avec Wireshark

Vous utiliserez les IPs suivantes :

| Machine           | Adresse IP    |
| ----------------- | ------------- |
| `node1.tp1.efrei` | `10.1.1.1/24` |
| `node2.tp1.efrei` | `10.1.1.2/24` |

🌞 **Déterminer l'adresse MAC de vos deux machines**

- depuis le terminal des machines Linux
- une seule commande est nécessaire

🌞 **Définir une IP statique sur les deux machines**

- depuis le terminal des machines Linux
- indiquez dans le compte-rendu l'ensemble des commandes réalisées
- montrez le contenu des fichiers que vous éditez (si vous en éditez)
- prouver que votre changement d'IP est effectif, en une commande

🌞 **Effectuer un `ping` d'une machine à l'autre**

- c'est la commande `ping`, sans surprise vous me direz

🌞 **Wireshark !**

- vous pouvez faire un clic droit sur un câble dans Wireshark pour lancer une capture des trames qui passent dans le câble
- visualiser le `ping` entre les deux machines
- enregistrez la capture avec Wireshark (format `.pcap` ou `.pcapng`), et vous la joindrez au compte-rendu dans le dépôt git
- précisez dans le compte-rendu quel protocole est utilisé pour envoyer le message `ping`

🌞 **ARP**

- un échange ARP a été nécessaire pour que le `ping` fonctionne
- utilisez une commande depuis `node1.tp1.efrei` pour connaître la MAC de son correspondant `node2.tp1.efrei`

# II. Ajoutons un switch

![Topologie n°2](./img/topo2.png)

> *VM Linux ou VPCS, libre à vous !*

Un switch vient résoudre une problématique simple : comment relier + de deux machines entre elles ? Le switch agit comme une simple multiprise réseau (dans son fonctionnement basique du moins ; un switch moderne possède des fonctionnalités plus avancées).

Le switch n'est pas vraiment un membre du réseau : il n'a pas d'adresse IP, on ne peut pas directement lui envoyer de message. Il se charge simplement de faire passer les messages d'une machine à une autre lorsqu'elles souhaitent discuter.

On va commencer simple : GNS3 fournit des switches tout nuls, prêts à l'emploi.

> *Vous pouvez réutiliser les machines de la partie précédente.*

| Machine           | Adresse IP    |
| ----------------- | ------------- |
| `node1.tp1.efrei` | `10.1.1.1/24` |
| `node2.tp1.efrei` | `10.1.1.2/24` |
| `node3.tp1.efrei` | `10.1.1.3/24` |

🌞 **Déterminer l'adresse MAC de vos trois machines**

🌞 **Définir une IP statique sur les trois machines**

- prouver que votre changement d'IP est effectif, en une commande

🌞 **Effectuer des `ping` d'une machine à l'autre**

- vérifiez que tout le monde peut se joindre
  - `node1` à `node2`
  - `node2` à `node3`
  - `node1` à `node3`

> Le message `ping` attend une réponse : `pong`. Ainsi, dans un setup aussi simple, inutile de tester `node2` vers `node1` si on a déjà testé `node1` vers `node2`. En effet, lorsque `node2` a reçu le `ping` de `node1`, il a répondu par un `pong`. On est donc déjà assurés que ça fonctionne correctement dans les deux sens.

# III. Serveur DHCP

## 1. Legit

![Topologie n°3](./img/topo3.png)

> *VM Linux ou VPCS, libre à vous ! Excepté le serveur DHCP qui DOIT être une machine Linux. Je vous recommande encore une fois Rocky Linux.*

Pour finir ce premier TP, on va mettre en place une 4ème machine : un serveur DHCP.

Le serveur DHCP est chargé d'attribuer des IPs à des clients qui le demandent. Ca évite la tâche fastidieuse de saisir une IP manuellement.

| Machine           | Adresse IP      |
| ----------------- | --------------- |
| `node1.tp1.efrei` | `N/A`           |
| `node2.tp1.efrei` | `N/A`           |
| `node3.tp1.efrei` | `N/A`           |
| `dhcp.tp1.efrei`  | `10.1.1.253/24` |

> Les IPs des trois nodes ne sont plus renseignées car le but de cette partie va être de faire en sorte qu'il puisse obtenir automatiquement une IP disponible, qui n'est pas déjà utilisée au sein du réseau, grâce au serveur DHCP.

🌞 **Donner un accès Internet à la machine `dhcp.tp1.efrei`**

- pour ce faire, ajoutez une carte réseau NAT à la machine dans VirtualBox
- une fois la machine démarrée, prouvez en une commande que vous avez un accès internet

Cet ajout de carte NAT est temporaire : c'est juste pour installer le paquet nécessaire pour le serveur DHCP. Dès que vous avez passer votre commande `dnf install`, **IL FAUDRA** enlever la carte NAT et retourner dans le setup normal.

> Très vite dans les TPs, on mettra un accès internet direct à l'aide de notre topologie, en incluant des routeurs. On trick pour ce TP1 en passant par une carte NAT :)

🌞 **Installer et configurer un serveur DHCP**

- à réaliser sur `dhcp.tp1.efrei`
- je n'aime pas ré-écrire la roue, et préfère pour vous renvoyer vers des ressources dispos en ligne quand elles sont suffisantes
- go google "rocky linux 9 dhcp server" ou utilisez [**cet article**](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=dhcp&f=1)
- ne tapez les commandes que si vous comprenez à quoi elles servent
- votre serveur DHCP doit attribuer des IP entre `10.1.1.10` et `10.1.1.50`

> **N'oubliez pas d'enlever la carte NAT et remettre dans le setup initial une fois que vous avez passé votre commande `dnf install`.**

🌞 **Récupérer une IP automatiquement depuis les 3 nodes**

- là encore, montrez toutes les commandes réalisées
- et le contenu des fichiers que vous éditez, si vous en éditez
- prouver que votre changement d'IP est effectif, en une commande

🌞 **Wireshark !**

- vous pouvez faire un clic droit sur un câble dans GNS, pour lancer une capture
- mettez en évidence l'échange qui est réalisé pour qu'une machine récupère une IP en DHCP
- l'échange est constitué de 4 messages, échangés entre le client et le serveur DHCP
- *hint* : on appelle souvent cet échange DORA
- une fois que vous avez visualisé cet échange, enregistrez la capture avec Wireshark, et joignez-la au compte rendu

## 2. DHCP spoofing

Une attaque qui consiste à se faire passer pour le serveur DHCP du réseau.

➜ **Introduire une nouvelle VM dans la topologie, OS de votre choix**

- ce sera notre machine attaquante
- branchez-la au switch
- installez dnsmasq sur la machine : un serveur DHCP (et DNS) performant
- ce sera notre "rogue DHCP server" : serveur DHCP malveillant

🌞 **Configurez dnsmasq**

- il doit uniquement faire serveur DHCP (car il peut aussi faire serveur DNS)
- il doit attribuer des adresses IP entre  `10.1.1.210` et `10.1.1.250`

🌞 **Test !**

- coupez le serveur DHCP "légitime" sur `dhcp.tp1.efrei`
- vérifier qu'un client (VPCS) récupère bien une adresse IP dans la range configurée avec dnsmasq

🌞 **Now race !**

- rallumez le serveur DHCP légitime
- demandez une IP avec un client (VPCS) et voyez qui répond
- faites-le plusieurs fois pour voir si c'est consistant
- je vous conseille de pop un nouveau VPCS à chaque fois, c'est très rapide

🌞 **Wireshark !**

- capturez cette course :d
- je veux une capture wireshark `race.pcap` qui montre les deux serveurs DHCP qui répondent

> *Si on met vraiment l'attaque en place et qu'on veut gagner la course, on n'hésite pas à mettre un coup de batte dans les jambes du concurrent : essayer de ralentir le serveur DHCP légitime. On abordera ça plus tard maybe, je vous invite fort à faire des recherches sur le sujet : comment ralentir une machine qu'on peut joindre sur le réseau, et spécifiquement un serveur DHCP ici. Aussi on remettra en place l'attaque dans des scénarios où on usurpe aussi l'identité du routeur.*

## 3. BONUS : DHCP starvation

Une attaque très débile et simple à mettre en place pour **DOS l'accès à un LAN** s'il n'y a pas de protections particulières. **C'est naze, mais c'est là** :d

Le principe est simple : **faire de multiples échanges DORA avec le serveur DHCP pour récupérer toutes les IP disponibles dans le réseau.**

On usurpe une adresse MAC (qu'elle existe ou non), on demande une adresse IP, on la récupère (merci). On répète l'opération avec une nouvelle fake adresse MAC, une nouvelle IP (merci). Etc. Jusqu'à épuiser toutes les adresses de la range.

Il existe des tools pour faire ça, vous pouvez aussi essayer (recommandé) de le **coder vous-mêmes avec Scapy** (une dinguerie cette lib) : on peut forger à peu près tout et n'importe quoi comme trame, et très facilement, avec Scapy.
