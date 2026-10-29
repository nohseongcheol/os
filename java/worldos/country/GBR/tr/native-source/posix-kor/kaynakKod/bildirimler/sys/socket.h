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
int socket(int 주소체계, int ağ_Tip, int 규약번호);
int bind(int Dosya_tanımlayıcı, const struct sockaddr *ADRES, socklen_t ADRES_süre);
ssize_t sendto(int Dosya_tanımlayıcı, const void *veri, size_t bayt_BAĞ_DEĞ_SAY, int Ayarlar,
               const struct sockaddr *ADRES, socklen_t ADRES_süre);
ssize_t recvfrom(int Dosya_tanımlayıcı, void *veri, size_t bayt_BAĞ_DEĞ_SAY, int Ayarlar,
                 struct sockaddr *ADRES, socklen_t *ADRES_süre);
int getsockname(int Dosya_tanımlayıcı, struct sockaddr *ADRES, socklen_t *ADRES_süre);
int setsockopt(int Dosya_tanımlayıcı, int katman_değer_e65604ef, int Ayarlar_ad, const void *değer, socklen_t değer_süre);
#endif
