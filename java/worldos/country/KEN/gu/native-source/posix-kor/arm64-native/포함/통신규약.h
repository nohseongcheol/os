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

/* ગુજરાતી 자료형은 મૅક્રો_મૂલ્ય 별칭이 아닌 독립된 구조체다.
 * સરનામું(住所)는 도착할 곳, 갈래는 સરનામું ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય, 전문(電文)은 경계 있는 통신 자료다. */
enum નેટવર્ક_અચલ {
    ક્લાઉડ_કુટુંબ = 2, સ્ટ્રીમ_નેટવર્ક = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t સરનામું_કુટુંબ; unsigned char સરનામું_ડેટા[14]; };
struct ઇન્ટરનેટ_સરનામું_મૂલ્ય { uint32_t સરનામું_મૂલ્ય; };
struct 인터넷통신주소 {
    uint16_t સરનામું_કુટુંબ;
    uint16_t પોર્ટ_નંબર;
    struct ઇન્ટરનેટ_સરનામું_મૂલ્ય ઇન્ટરનેટ_સરનામું;
    unsigned char હાંસિયો_મૂલ્ય[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,ઇન્ટરનેટ_સરનામું)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int સરનામું_કુટુંબ, int 통신방식, int સ્થાનાંતર_પ્રોટોકૉલ);
int બાઇંડ_કરો_સરનામું(int 종단, const struct 통신주소 *સરનામું, 통신주소길이형 લંબાઈ_મૂલ્ય);
intptr_t 자료전문보내기(int 종단, const void *ડેટા, size_t 개수, int ચયન_મૂલ્ય, const struct 통신주소 *સરનામું, 통신주소길이형 લંબાઈ_મૂલ્ય);
intptr_t 자료전문받기(int 종단, void *ડેટા, size_t 개수, int ચયન_મૂલ્ય, struct 통신주소 *સરનામું, 통신주소길이형 *લંબાઈ_મૂલ્ય);
int 통신주소읽기(int 종단, struct 통신주소 *સરનામું, 통신주소길이형 *લંબાઈ_મૂલ્ય);
int કનેક્ટ_નેટવર્ક(int 종단, const struct 통신주소 *સરનામું, 통신주소길이형 લંબાઈ_મૂલ્ય);
int 통신연결기다리기(int 종단, int 대기수);
int સ્વીકારો_નેટવર્ક_કનેક્શન(int 종단, struct 통신주소 *સરનામું, 통신주소길이형 *લંબાઈ_મૂલ્ય);

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
static inline uint16_t 망차례짧은수(uint16_t મૂલ્ય) { return (uint16_t)((મૂલ્ય >> 8) | (મૂલ્ય << 8)); }
static inline uint32_t નેટવર્ક_પૂર્ણાંક(uint32_t મૂલ્ય) { return ((મૂલ્ય & 255u) << 24) | ((મૂલ્ય & 0xff00u) << 8) | ((મૂલ્ય >> 8) & 0xff00u) | (મૂલ્ય >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t મૂલ્ય) { return 망차례짧은수(મૂલ્ય); }
static inline uint32_t ડિવાઇસ_ક્રમ_પૂર્ણાંક(uint32_t મૂલ્ય) { return નેટવર્ક_પૂર્ણાંક(મૂલ્ય); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return નેટવર્ક_પૂર્ણાંક(x); }
#endif
