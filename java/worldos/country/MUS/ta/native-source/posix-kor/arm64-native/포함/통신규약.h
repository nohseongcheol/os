#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 செயல்படுத்தக்கூடிய_கோப்பு·외부 코드와 연결할 때만 사용한다. */
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

/* தமிழ் 자료형은 மேக்ரோ_மதிப்பு 별칭이 아닌 독립된 구조체다.
 * முகவரி(住所)는 도착할 곳, 갈래는 முகவரி இயக்க_முறைமை_மதிப்பு, 전문(電文)은 경계 있는 통신 자료다. */
enum பிணையம்_மாறிலி {
    இணையம்_குடும்பம் = 2, தொடரோடி_பிணையம் = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t முகவரி_குடும்பம்; unsigned char முகவரி_தரவு[14]; };
struct இணைய_முகவரி_மதிப்பு { uint32_t முகவரி_மதிப்பு; };
struct 인터넷통신주소 {
    uint16_t முகவரி_குடும்பம்;
    uint16_t முனைய_எண்;
    struct இணைய_முகவரி_மதிப்பு இணைய_முகவரி;
    unsigned char ஓரம்_மதிப்பு[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,இணைய_முகவரி)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int உருவாக்கு_முடிவுப்_புள்ளி(int முகவரி_குடும்பம், int 통신방식, int இடமாற்று_நெறிமுறை);
int கட்டு_முகவரி(int முடிவுப்_புள்ளி, const struct 통신주소 *முகவரி, 통신주소길이형 நீளம்_மதிப்பு);
intptr_t 자료전문보내기(int முடிவுப்_புள்ளி, const void *தரவு, size_t 개수, int தேர்வு_மதிப்பு, const struct 통신주소 *முகவரி, 통신주소길이형 நீளம்_மதிப்பு);
intptr_t 자료전문받기(int முடிவுப்_புள்ளி, void *தரவு, size_t 개수, int தேர்வு_மதிப்பு, struct 통신주소 *முகவரி, 통신주소길이형 *நீளம்_மதிப்பு);
int 통신주소읽기(int முடிவுப்_புள்ளி, struct 통신주소 *முகவரி, 통신주소길이형 *நீளம்_மதிப்பு);
int இணை_பிணையம்(int முடிவுப்_புள்ளி, const struct 통신주소 *முகவரி, 통신주소길이형 நீளம்_மதிப்பு);
int 통신연결기다리기(int முடிவுப்_புள்ளி, int 대기수);
int ஏற்றுக்கொள்_நெட்வொர்க்_இணைப்பு(int முடிவுப்_புள்ளி, struct 통신주소 *முகவரி, 통신주소길이형 *நீளம்_மதிப்பு);

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
static inline uint16_t 망차례짧은수(uint16_t மதிப்பு) { return (uint16_t)((மதிப்பு >> 8) | (மதிப்பு << 8)); }
static inline uint32_t பிணையம்_முழு_எண்(uint32_t மதிப்பு) { return ((மதிப்பு & 255u) << 24) | ((மதிப்பு & 0xff00u) << 8) | ((மதிப்பு >> 8) & 0xff00u) | (மதிப்பு >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t மதிப்பு) { return 망차례짧은수(மதிப்பு); }
static inline uint32_t சாதனம்_வரிசை_முழு_எண்(uint32_t மதிப்பு) { return பிணையம்_முழு_எண்(மதிப்பு); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return பிணையம்_முழு_எண்(x); }
#endif
