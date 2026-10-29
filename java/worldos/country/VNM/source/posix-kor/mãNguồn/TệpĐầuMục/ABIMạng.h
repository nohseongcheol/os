#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define tạoĐiểmCuối socket
#define ràngBuộcĐịaChỉ bind
#define gửiDữLiệuĐiệnDữLiệu sendto
#define nhậnDữLiệuĐiệnDữLiệu recvfrom
#define đọcĐịaChỉỔCắmMạng getsockname
#define đổiCácThiếtLậpMạng setsockopt
#define phânTíchCúPhápĐịaChỉMạng inet_pton
#define địaChỉMạngĐịnhDạng inet_ntop
#define ngắnKiểuMạng htons
#define sốNguyênMạng htonl
#define ngắnKiểuThứTựThiếtBị ntohs
#define sốNguyênThứTựThiếtBị ntohl
#endif
