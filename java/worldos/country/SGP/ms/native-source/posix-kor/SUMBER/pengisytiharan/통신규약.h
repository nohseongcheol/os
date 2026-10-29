#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define cipta_peserta socket
#define ikat_e_mel bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ubah_rangkaian_Seting setsockopt
#define hurai_rangkaian_e_mel inet_pton
#define format_rangkaian_e_mel inet_ntop
#define 망차례짧은수 htons
#define rangkaian_integer htonl
#define 장치차례짧은수 ntohs
#define peranti_tertib_integer ntohl
#endif
