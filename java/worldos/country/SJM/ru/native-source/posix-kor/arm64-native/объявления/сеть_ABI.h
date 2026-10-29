#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "файл_ABI.h"
/* 표준 ABI는 기존 исполняемый_файл·внешний_ЗНАЧЕН 코드와 연결할 때만 사용한다. */
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

/* русский 자료형은 макрос_ЗНАЧЕН 별칭이 아닌 독립된 구조체다.
 * АДРЕС(住所)는 도착할 곳, 갈래는 АДРЕС операционная_система_ЗНАЧЕН, датаграмма(電文)은 граница_ЗНАЧЕН 있는 коммуникация 자료다. */
enum сеть_константа {
    облако_Семья = 2, поток_сеть = 1, сокет_датаграмм = 2,
    поток_транспортный_протокол = 6, датаграмма_протокол = 17,
    петлевой_адрес = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t сокет_АДРЕС_длина_ТИП;
struct сокет_АДРЕС { uint16_t АДРЕС_Семья; unsigned char АДРЕС_данные[14]; };
struct адрес_в_Интернете_ЗНАЧЕН { uint32_t АДРЕС_ЗНАЧЕН; };
struct облако_сокет_АДРЕС {
    uint16_t АДРЕС_Семья;
    uint16_t номер_порта;
    struct адрес_в_Интернете_ЗНАЧЕН адрес_в_Интернете;
    unsigned char поле_ЗНАЧЕН[8];
};
typedef struct сокет_АДРЕС сокет_АДРЕС_ТИП;
typedef struct облако_сокет_АДРЕС облако_сокет_АДРЕС_ТИП;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char чек_облако_сокет_АДРЕС_изменить_размер[(sizeof(struct облако_сокет_АДРЕС)==16)?1:-1];
typedef char чек_облако_сокет_АДРЕС_Макет[(offsetof(struct облако_сокет_АДРЕС,адрес_в_Интернете)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Create_участник(int АДРЕС_Семья, int коммуникация_МОДА, int передать_протокол);
int BIND_АДРЕС(int участник, const struct сокет_АДРЕС *АДРЕС, сокет_АДРЕС_длина_ТИП длина_ЗНАЧЕН);
intptr_t написать_датаграмма_данные(int участник, const void *данные, size_t товар_СЧЁТ, int выделение_ЗНАЧЕН, const struct сокет_АДРЕС *АДРЕС, сокет_АДРЕС_длина_ТИП длина_ЗНАЧЕН);
intptr_t получить_датаграмма_данные(int участник, void *данные, size_t товар_СЧЁТ, int выделение_ЗНАЧЕН, struct сокет_АДРЕС *АДРЕС, сокет_АДРЕС_длина_ТИП *длина_ЗНАЧЕН);
int чтение_сокет_АДРЕС(int участник, struct сокет_АДРЕС *АДРЕС, сокет_АДРЕС_длина_ТИП *длина_ЗНАЧЕН);
int Connect_сеть(int участник, const struct сокет_АДРЕС *АДРЕС, сокет_АДРЕС_длина_ТИП длина_ЗНАЧЕН);
int 통신연결기다리기(int участник, int Заждался_СЧЁТ);
int принять_сетевое_подключение(int участник, struct сокет_АДРЕС *АДРЕС, сокет_АДРЕС_длина_ТИП *длина_ЗНАЧЕН);

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
static inline uint16_t 망차례짧은수(uint16_t ЗНАЧЕН) { return (uint16_t)((ЗНАЧЕН >> 8) | (ЗНАЧЕН << 8)); }
static inline uint32_t сеть_целое_число(uint32_t ЗНАЧЕН) { return ((ЗНАЧЕН & 255u) << 24) | ((ЗНАЧЕН & 0xff00u) << 8) | ((ЗНАЧЕН >> 8) & 0xff00u) | (ЗНАЧЕН >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t ЗНАЧЕН) { return 망차례짧은수(ЗНАЧЕН); }
static inline uint32_t устройство_заказ_целое_число(uint32_t ЗНАЧЕН) { return сеть_целое_число(ЗНАЧЕН); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return сеть_целое_число(x); }
#endif
