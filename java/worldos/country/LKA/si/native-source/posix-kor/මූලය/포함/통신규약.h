#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define බඳින්න_යොමුව bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define වෙනස්_කරන්න_ජාලය_පසුතල setsockopt
#define විශ්ලේෂණය_කරන්න_ජාලය_යොමුව inet_pton
#define හැඩතලය_ජාලය_යොමුව inet_ntop
#define 망차례짧은수 htons
#define ජාලය_පූර්ණාංකය htonl
#define 장치차례짧은수 ntohs
#define ජංගම_අනුපිළිවෙළ_පූර්ණාංකය ntohl
#endif
