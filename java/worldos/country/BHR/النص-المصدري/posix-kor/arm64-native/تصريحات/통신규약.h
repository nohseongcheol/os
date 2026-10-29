#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·خارجي_قيمة 코드와 연결할 때만 사용한다. */
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

/* العربية 자료형은 ماكرو_قيمة 별칭이 아닌 독립된 구조체다.
 * عنوان(住所)는 도착할 곳, 갈래는 عنوان نظام_تشغيل_قيمة, رزمةمستقلة(電文)은 경계 있는 통신 자료다. */
enum شبكة_ثابت {
    سحابة_عائلة = 2, بث_شبكة = 1, مأخذ_مخطط_البيانات = 2,
    بث_بروتوكول_النقل = 6, مخطط_بيانات_بروتوكول = 17,
    عنوان_الاسترجاع = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct مأخذ_التوصيل_عنوان { uint16_t عنوان_عائلة; unsigned char عنوان_بيانات[14]; };
struct عنوان_الإنترنت_قيمة { uint32_t عنوان_قيمة; };
struct سحابة_مأخذ_التوصيل_عنوان {
    uint16_t عنوان_عائلة;
    uint16_t رقم_المنفذ;
    struct عنوان_الإنترنت_قيمة عنوان_الإنترنت;
    unsigned char هامش_قيمة[8];
};
typedef struct مأخذ_التوصيل_عنوان مأخذ_التوصيل_عنوان_نوع;
typedef struct سحابة_مأخذ_التوصيل_عنوان سحابة_مأخذ_التوصيل_عنوان_نوع;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char شيك_سحابة_مأخذ_التوصيل_عنوان_يغير_الحجم[(sizeof(struct سحابة_مأخذ_التوصيل_عنوان)==16)?1:-1];
typedef char شيك_سحابة_مأخذ_التوصيل_عنوان_تخطيط[(offsetof(struct سحابة_مأخذ_التوصيل_عنوان,عنوان_الإنترنت)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int فتح_المشارك(int عنوان_عائلة, int 통신방식, int نقل_بروتوكول);
int يربط_عنوان(int المشارك, const struct مأخذ_التوصيل_عنوان *عنوان, 통신주소길이형 길이);
intptr_t يرسل_مخطط_بيانات_بيانات(int المشارك, const void *بيانات, size_t 개수, int تحديد_قيمة, const struct مأخذ_التوصيل_عنوان *عنوان, 통신주소길이형 길이);
intptr_t يستلم_مخطط_بيانات_بيانات(int المشارك, void *بيانات, size_t 개수, int تحديد_قيمة, struct مأخذ_التوصيل_عنوان *عنوان, 통신주소길이형 *길이);
int يقرأ_مأخذ_التوصيل_عنوان(int المشارك, struct مأخذ_التوصيل_عنوان *عنوان, 통신주소길이형 *길이);
int يتصل_شبكة(int المشارك, const struct مأخذ_التوصيل_عنوان *عنوان, 통신주소길이형 길이);
int 통신연결기다리기(int المشارك, int 대기수);
int قبول_اتصال_الشبكة(int المشارك, struct مأخذ_التوصيل_عنوان *عنوان, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t قيمة) { return (uint16_t)((قيمة >> 8) | (قيمة << 8)); }
static inline uint32_t شبكة_عدد_صحيح(uint32_t قيمة) { return ((قيمة & 255u) << 24) | ((قيمة & 0xff00u) << 8) | ((قيمة >> 8) & 0xff00u) | (قيمة >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t قيمة) { return 망차례짧은수(قيمة); }
static inline uint32_t جهاز_أمر_عدد_صحيح(uint32_t قيمة) { return شبكة_عدد_صحيح(قيمة); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return شبكة_عدد_صحيح(x); }
#endif
