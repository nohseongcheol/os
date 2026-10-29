#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·зовнішній_значення 코드와 연결할 때만 사용한다. */
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

/* українська 자료형은 макрос_значення 별칭이 아닌 독립된 구조체다.
 * Адреса(住所)는 도착할 곳, 갈래는 Адреса операційна_система_ОС_значення, дейтаграма(電文)은 경계 있는 통신 자료다. */
enum мережа_константа {
    хмара_сім_я = 2, потік_мережа = 1, сокет_дейтаграми = 2,
    потік_транспортний_протокол = 6, дейтаграма_протокол = 17,
    адреса_замикання_на_себе = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct сокет_адреса { uint16_t адреса_сім_я; unsigned char адреса_дані[14]; };
struct адреса_в_Інтернеті_значення { uint32_t адреса_значення; };
struct хмара_сокет_адреса {
    uint16_t адреса_сім_я;
    uint16_t номер_порту;
    struct адреса_в_Інтернеті_значення адреса_в_Інтернеті;
    unsigned char поле_значення[8];
};
typedef struct сокет_адреса сокет_адреса_Тип;
typedef struct хмара_сокет_адреса хмара_сокет_адреса_Тип;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char перевіряти_хмара_сокет_адреса_змінювати_розмір[(sizeof(struct хмара_сокет_адреса)==16)?1:-1];
typedef char перевіряти_хмара_сокет_адреса_Макет[(offsetof(struct хмара_сокет_адреса,адреса_в_Інтернеті)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Створення_учасник(int адреса_сім_я, int 통신방식, int передача_протокол);
int зв_язувати_адреса(int учасник, const struct сокет_адреса *Адреса, 통신주소길이형 길이);
intptr_t надсилати_дейтаграма_дані(int учасник, const void *дані, size_t 개수, int вибране_значення, const struct сокет_адреса *Адреса, 통신주소길이형 길이);
intptr_t отримувати_дейтаграма_дані(int учасник, void *дані, size_t 개수, int вибране_значення, struct сокет_адреса *Адреса, 통신주소길이형 *길이);
int 통신주소읽기(int учасник, struct сокет_адреса *Адреса, 통신주소길이형 *길이);
int зв_язок_мережа(int учасник, const struct сокет_адреса *Адреса, 통신주소길이형 길이);
int 통신연결기다리기(int учасник, int 대기수);
int приймати_підключення_до_мережі(int учасник, struct сокет_адреса *Адреса, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t значення) { return (uint16_t)((значення >> 8) | (значення << 8)); }
static inline uint32_t мережа_ціле_число(uint32_t значення) { return ((значення & 255u) << 24) | ((значення & 0xff00u) << 8) | ((значення >> 8) & 0xff00u) | (значення >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t значення) { return 망차례짧은수(значення); }
static inline uint32_t пристрій_порядок_ціле_число(uint32_t значення) { return мережа_ціле_число(значення); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return мережа_ціле_число(x); }
#endif
