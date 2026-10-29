#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·외부 코드와 연결할 때만 사용한다. */
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

/* اردو 자료형은 میکرو_قدر 별칭이 아닌 독립된 구조체다.
 * پتہ(住所)는 도착할 곳, 갈래는 پتہ آپریٹنگ_سسٹم_قدر, 전문(電文)은 경계 있는 통신 자료다. */
enum نیٹ_ورک_مستقل {
    بادل_خاندان = 2, بہاؤ_نیٹ_ورک = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t پتہ_خاندان; unsigned char پتہ_کوائف[14]; };
struct انٹرنیٹ_پتہ_قدر { uint32_t پتہ_قدر; };
struct 인터넷통신주소 {
    uint16_t پتہ_خاندان;
    uint16_t دہانہ_نمبر;
    struct انٹرنیٹ_پتہ_قدر انٹرنیٹ_پتہ;
    unsigned char حاشیہ_قدر[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,انٹرنیٹ_پتہ)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int پتہ_خاندان, int 통신방식, int منتقلی_پروٹوکول);
int باندھیں_پتہ(int 종단, const struct 통신주소 *پتہ, 통신주소길이형 لمبا_ئی_قدر);
intptr_t 자료전문보내기(int 종단, const void *کوائف, size_t 개수, int انتخاب_قدر, const struct 통신주소 *پتہ, 통신주소길이형 لمبا_ئی_قدر);
intptr_t 자료전문받기(int 종단, void *کوائف, size_t 개수, int انتخاب_قدر, struct 통신주소 *پتہ, 통신주소길이형 *لمبا_ئی_قدر);
int 통신주소읽기(int 종단, struct 통신주소 *پتہ, 통신주소길이형 *لمبا_ئی_قدر);
int جڑیں_نیٹ_ورک(int 종단, const struct 통신주소 *پتہ, 통신주소길이형 لمبا_ئی_قدر);
int 통신연결기다리기(int 종단, int 대기수);
int قبول_کریں_نیٹ_ورک_کنکشن(int 종단, struct 통신주소 *پتہ, 통신주소길이형 *لمبا_ئی_قدر);

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
static inline uint16_t 망차례짧은수(uint16_t قدر) { return (uint16_t)((قدر >> 8) | (قدر << 8)); }
static inline uint32_t نیٹ_ورک_سالم_عدد(uint32_t قدر) { return ((قدر & 255u) << 24) | ((قدر & 0xff00u) << 8) | ((قدر >> 8) & 0xff00u) | (قدر >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t قدر) { return 망차례짧은수(قدر); }
static inline uint32_t آلہ_ترتیم_سالم_عدد(uint32_t قدر) { return نیٹ_ورک_سالم_عدد(قدر); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return نیٹ_ورک_سالم_عدد(x); }
#endif
