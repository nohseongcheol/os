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
int socket(int 주소체계, int rede_Tipo, int contrato_número);
int bind(int Arquivo_descritor, const struct sockaddr *Endereço, socklen_t email_duração);
ssize_t sendto(int Arquivo_descritor, const void *dados, size_t byte_CONT_NÚM, int Definições,
               const struct sockaddr *Endereço, socklen_t email_duração);
ssize_t recvfrom(int Arquivo_descritor, void *dados, size_t byte_CONT_NÚM, int Definições,
                 struct sockaddr *Endereço, socklen_t *email_duração);
int getsockname(int Arquivo_descritor, struct sockaddr *Endereço, socklen_t *email_duração);
int setsockopt(int Arquivo_descritor, int camada_VALOR, int Configurações_nome, const void *VALOR, socklen_t VALOR_duração);
#endif
