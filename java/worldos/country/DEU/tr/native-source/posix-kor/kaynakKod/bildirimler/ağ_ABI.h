#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define açmak_uç_nokta socket
#define BIND_ADRES bind
#define göndermek_veri_birimi_veri sendto
#define almak_veri_birimi_veri recvfrom
#define 통신주소읽기 getsockname
#define değiştirmek_ağ_Ayarlar setsockopt
#define ayrıştırmak_ağ_kimliği inet_pton
#define biçim_ağ_kimliği inet_ntop
#define 망차례짧은수 htons
#define ağ_bilgi htonl
#define 장치차례짧은수 ntohs
#define cihaz_düzen_bilgi ntohl
#endif
