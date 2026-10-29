#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_ADDRESS bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define athraigh_Líonra_Socruithe setsockopt
#define parsáil_Líonra_ADDRESS inet_pton
#define formáid_Líonra_ADDRESS inet_ntop
#define 망차례짧은수 htons
#define Líonra_slánuimhir htonl
#define 장치차례짧은수 ntohs
#define gléas_ord_slánuimhir ntohl
#endif
