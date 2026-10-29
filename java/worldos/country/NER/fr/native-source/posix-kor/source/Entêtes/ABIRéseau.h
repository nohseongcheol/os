#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define créerExtrémité socket
#define associerAdresse bind
#define envoyerDonnéesDatagramme sendto
#define recevoirDonnéesDatagramme recvfrom
#define lireAdressePriseRéseau getsockname
#define changerRéglagesRéseau setsockopt
#define analyserAdresseRéseau inet_pton
#define adresseRéseauFormat inet_ntop
#define courtRéseau htons
#define entierRéseau htonl
#define courtOrdrePériphérique ntohs
#define entierOrdrePériphérique ntohl
#endif
