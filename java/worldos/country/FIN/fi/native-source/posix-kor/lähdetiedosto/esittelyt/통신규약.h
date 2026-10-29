#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Luo_päätepiste socket
#define BIND_OSOITE bind
#define lähettää_datagrammi_data sendto
#define saada_datagrammi_data recvfrom
#define lukea_vastake_OSOITE getsockname
#define muuttaa_verkko_Asetukset setsockopt
#define jäsentää_verkkotunnus inet_pton
#define muoto_verkkotunnus inet_ntop
#define 망차례짧은수 htons
#define verkko_kokonaisluku htonl
#define 장치차례짧은수 ntohs
#define laite_tilata_kokonaisluku ntohl
#endif
