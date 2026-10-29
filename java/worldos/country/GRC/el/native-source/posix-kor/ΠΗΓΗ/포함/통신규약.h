#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define ανοίγω_τελικό_σημείο socket
#define συνδέω_διεύθυνση bind
#define στέλνω_αυτοδύναμο_πακέτο_δεδομένα sendto
#define λαμβάνω_αυτοδύναμο_πακέτο_δεδομένα recvfrom
#define 통신주소읽기 getsockname
#define αλλάζω_δίκτυο_Ρυθμίσεις setsockopt
#define ανάλυση_αναγνωριστικό_δικτύου inet_pton
#define μορφή_αναγνωριστικό_δικτύου inet_ntop
#define 망차례짧은수 htons
#define δίκτυο_ακέραιος htonl
#define 장치차례짧은수 ntohs
#define συσκευή_σειρά_ακέραιος ntohl
#endif
