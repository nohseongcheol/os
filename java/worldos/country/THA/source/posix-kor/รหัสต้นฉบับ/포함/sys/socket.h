#ifndef JKOROS_SOCKET_H
#define JKOROS_SOCKET_H
#include <sys/types.h>
typedef unsigned int socklen_t;
typedef unsigned short sa_family_t;
struct sockaddr { sa_family_t sa_family; char sa_data[14]; };
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define MSG_DONTWAIT 64
#define SOL_SOCKET 1
#define SO_RCVTIMEO 20
int socket(int 주소체계, int 통신종류, int กรณี_หมายเลข);
int bind(int 파일서술자, const struct sockaddr *อีเมล, socklen_t 주소길이);
ssize_t sendto(int 파일서술자, const void *ข้อมูล, size_t 바이트수, int ตั้งค่า,
               const struct sockaddr *อีเมล, socklen_t 주소길이);
ssize_t recvfrom(int 파일서술자, void *ข้อมูล, size_t 바이트수, int ตั้งค่า,
                 struct sockaddr *อีเมล, socklen_t *주소길이);
int getsockname(int 파일서술자, struct sockaddr *อีเมล, socklen_t *주소길이);
int setsockopt(int 파일서술자, int เลเยอร์_ค่า, int การตั้งค่า_ชื่อ, const void *ค่า, socklen_t 값길이);
#endif
