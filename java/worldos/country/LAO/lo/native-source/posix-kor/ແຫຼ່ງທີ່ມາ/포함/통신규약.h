#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ຜູກ_ມັດ_ອີເມວ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ປ່ຽນ_ແປງ_ເຄືອຂ່າຍ_ການຕັ້ງຄ່າ setsockopt
#define ການແຈກຄໍາສັບ_ເຄືອຂ່າຍ_ອີເມວ inet_pton
#define ຮູບແບບ_ເຄືອຂ່າຍ_ອີເມວ inet_ntop
#define 망차례짧은수 htons
#define ເຄືອຂ່າຍ_ຕົວເລກຈໍານວນເຕັມ htonl
#define 장치차례짧은수 ntohs
#define ມືຖື_ລໍາດັບ_ຕົວເລກຈໍານວນເຕັມ ntohl
#endif
