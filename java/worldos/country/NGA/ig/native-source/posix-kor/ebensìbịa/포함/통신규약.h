#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define JIKỌNYE_àdreèsì bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define gbanwèe_Netwọọkụ_Mwube setsockopt
#define kerìsịa_Netwọọkụ_àdreèsì inet_pton
#define hàzie_Netwọọkụ_àdreèsì inet_ntop
#define 망차례짧은수 htons
#define Netwọọkụ_ọnụọgụ_nzùrùòkè htonl
#define 장치차례짧은수 ntohs
#define njìarụ_ùsòrò_ọnụọgụ_nzùrùòkè ntohl
#endif
