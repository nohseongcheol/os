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

/* 한국어 자료형은 макро_маани 별칭이 아닌 독립된 구조체다.
 * дарек(住所)는 도착할 곳, 갈래는 дарек оперативдик_система_маани, 전문(電文)은 경계 있는 통신 자료다. */
enum Желе_өзгөрбөс_чоңдук {
    Интернет_Үй_бүлө = 2, агым_Желе = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t дарек_Үй_бүлө; unsigned char дарек_берилмелер[14]; };
struct Интернет_дарек_маани { uint32_t дарек_маани; };
struct 인터넷통신주소 {
    uint16_t дарек_Үй_бүлө;
    uint16_t 접속번호;
    struct Интернет_дарек_маани Интернет_дарек;
    unsigned char чет_аянт_маани[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Интернет_дарек)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int дарек_Үй_бүлө, int 통신방식, int ташүү_протокол);
int байланыштыруу_дарек(int 종단, const struct 통신주소 *дарек, 통신주소길이형 узундук_маани);
intptr_t 자료전문보내기(int 종단, const void *берилмелер, size_t 개수, int белгилөө_маани, const struct 통신주소 *дарек, 통신주소길이형 узундук_маани);
intptr_t 자료전문받기(int 종단, void *берилмелер, size_t 개수, int белгилөө_маани, struct 통신주소 *дарек, 통신주소길이형 *узундук_маани);
int 통신주소읽기(int 종단, struct 통신주소 *дарек, 통신주소길이형 *узундук_маани);
int ТУТАШУУ_Желе(int 종단, const struct 통신주소 *дарек, 통신주소길이형 узундук_маани);
int 통신연결기다리기(int 종단, int 대기수);
int кабыл_алуу_желе_туташуусу(int 종단, struct 통신주소 *дарек, 통신주소길이형 *узундук_маани);

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
static inline uint16_t 망차례짧은수(uint16_t маани) { return (uint16_t)((маани >> 8) | (маани << 8)); }
static inline uint32_t Желе_бүтүн_сан(uint32_t маани) { return ((маани & 255u) << 24) | ((маани & 0xff00u) << 8) | ((маани >> 8) & 0xff00u) | (маани >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t маани) { return 망차례짧은수(маани); }
static inline uint32_t түзмөк_ылгоо_ирети_бүтүн_сан(uint32_t маани) { return Желе_бүтүн_сан(маани); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return Желе_бүтүн_сан(x); }
#endif
