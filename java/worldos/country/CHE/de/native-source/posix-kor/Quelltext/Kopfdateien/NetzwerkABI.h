#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define endpunktErstellen socket
#define adresseZuordnen bind
#define datagrammDatenSenden sendto
#define datagrammDatenEmpfangen recvfrom
#define netzbuchseAdresseLesen getsockname
#define netzwerkEinstellungenÄndern setsockopt
#define netzwerkAdresseAnalysieren inet_pton
#define formatNetzwerkAdresse inet_ntop
#define netzwerkKurz htons
#define netzwerkGanzzahl htonl
#define gerätReihenfolgeKurz ntohs
#define gerätReihenfolgeGanzzahl ntohl
#endif
