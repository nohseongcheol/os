#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Buat_peserta socket
#define ikat_surel bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ubah_jaringan_Pengaturan setsockopt
#define urai_jaringan_surel inet_pton
#define format_jaringan_surel inet_ntop
#define 망차례짧은수 htons
#define jaringan_bilangan_bulat htonl
#define 장치차례짧은수 ntohs
#define Ponsel_urutan_bilangan_bulat ntohl
#endif
