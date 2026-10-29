#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·externo_VALOR 코드와 연결할 때만 사용한다. */
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
#define IPPROTO_TCP 6
#define INADDR_LOOPBACK 0x7f000001u
typedef uint32_t pk_socklen_t;
struct pk_sockaddr { uint16_t sa_family; unsigned char sa_data[14]; };
struct pk_in_addr { uint32_t s_addr; };
struct pk_sockaddr_in { uint16_t sin_family, sin_port; struct pk_in_addr sin_addr; unsigned char sin_zero[8]; };

/* Galego 자료형은 macro_VALOR 별칭이 아닌 독립된 구조체다.
 * ENDEREZO(住所)는 도착할 곳, 갈래는 ENDEREZO sistema_operativo_VALOR, 전문(電文)은 경계 있는 통신 자료다. */
enum Rede_constante {
    nube_Familia = 2, fluxo_Rede = 1, 전문통신 = 2,
    fluxo_protocolo_de_transporte = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t ENDEREZO_Familia; unsigned char ENDEREZO_datos[14]; };
struct enderezo_de_internet_VALOR { uint32_t ENDEREZO_VALOR; };
struct 인터넷통신주소 {
    uint16_t ENDEREZO_Familia;
    uint16_t número_do_porto;
    struct enderezo_de_internet_VALOR enderezo_de_internet;
    unsigned char marxe_VALOR[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,enderezo_de_internet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int crear_extremo(int ENDEREZO_Familia, int 통신방식, int Transferir_protocolo);
int ligar_ENDEREZO(int extremo, const struct 통신주소 *ENDEREZO, 통신주소길이형 duración_VALOR);
intptr_t 자료전문보내기(int extremo, const void *datos, size_t elemento_CONTAR, int selección_VALOR, const struct 통신주소 *ENDEREZO, 통신주소길이형 duración_VALOR);
intptr_t 자료전문받기(int extremo, void *datos, size_t elemento_CONTAR, int selección_VALOR, struct 통신주소 *ENDEREZO, 통신주소길이형 *duración_VALOR);
int 통신주소읽기(int extremo, struct 통신주소 *ENDEREZO, 통신주소길이형 *duración_VALOR);
int CONECTAR_Rede(int extremo, const struct 통신주소 *ENDEREZO, 통신주소길이형 duración_VALOR);
int 통신연결기다리기(int extremo, int Agardando_CONTAR);
int aceptar_conexión_de_rede(int extremo, struct 통신주소 *ENDEREZO, 통신주소길이형 *duración_VALOR);

int pk_connect(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
int pk_listen(int fd, int backlog);
int pk_accept(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_socket(int domain, int type, int protocol);
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
#ifdef __cplusplus
}
#endif
static inline uint16_t 망차례짧은수(uint16_t VALOR) { return (uint16_t)((VALOR >> 8) | (VALOR << 8)); }
static inline uint32_t Rede_número_enteiro(uint32_t VALOR) { return ((VALOR & 255u) << 24) | ((VALOR & 0xff00u) << 8) | ((VALOR >> 8) & 0xff00u) | (VALOR >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALOR) { return 망차례짧은수(VALOR); }
static inline uint32_t dispositivo_orde_número_enteiro(uint32_t VALOR) { return Rede_número_enteiro(VALOR); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return Rede_número_enteiro(x); }
#endif
