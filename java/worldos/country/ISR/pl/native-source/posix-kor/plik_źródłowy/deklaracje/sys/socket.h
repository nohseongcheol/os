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
int socket(int 주소체계, int sieć_Rodzaj, int sprawa_identyfikator);
int bind(int Plik_deskryptor, const struct sockaddr *Adres, socklen_t ADRES_długość);
ssize_t sendto(int Plik_deskryptor, const void *dane, size_t bajt_ILE_LICZB, int Ustawienia,
               const struct sockaddr *Adres, socklen_t ADRES_długość);
ssize_t recvfrom(int Plik_deskryptor, void *dane, size_t bajt_ILE_LICZB, int Ustawienia,
                 struct sockaddr *Adres, socklen_t *ADRES_długość);
int getsockname(int Plik_deskryptor, struct sockaddr *Adres, socklen_t *ADRES_długość);
int setsockopt(int Plik_deskryptor, int warstwa_WARTOŚĆ, int Ustawienia_nazwa, const void *WARTOŚĆ, socklen_t WARTOŚĆ_długość);
#endif
