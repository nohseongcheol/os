#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 നിര്_വ്വഹണക്ഷമമായ_ഫയല്·외부 코드와 연결할 때만 사용한다. */
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

/* 한국어 자료형은 മാക്രോ_മൂല്യം 별칭이 아닌 독립된 구조체다.
 * ഇമെയിൽ(住所)는 도착할 곳, 갈래는 ഇമെയിൽ ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം, 전문(電文)은 경계 있는 통신 자료다. */
enum നെറ്റ്_വർക്ക്_സ്ഥിരം {
    ക്ലൌഡ്_കുടുംബം = 2, സ്ട്രീം_നെറ്റ്_വർക്ക് = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t ഇമെയിൽ_കുടുംബം; unsigned char ഇമെയിൽ_ഡാറ്റാ[14]; };
struct ഇന്_റര്_നെറ്റ്_വിലാസം_മൂല്യം { uint32_t ഇമെയിൽ_മൂല്യം; };
struct 인터넷통신주소 {
    uint16_t ഇമെയിൽ_കുടുംബം;
    uint16_t പോര്_ട്ട്_നമ്പര്;
    struct ഇന്_റര്_നെറ്റ്_വിലാസം_മൂല്യം ഇന്_റര്_നെറ്റ്_വിലാസം;
    unsigned char മാര്_ജിന്_മൂല്യം[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,ഇന്_റര്_നെറ്റ്_വിലാസം)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int സൃഷ്_ടിക്കുക_അവസാനബിന്ദു(int ഇമെയിൽ_കുടുംബം, int 통신방식, int കൈമാറുക_പ്രോട്ടോക്കോള്);
int బైండ్_చేయి_ഇമെയിൽ(int അവസാനബിന്ദു, const struct 통신주소 *ഇമെയിൽ, 통신주소길이형 ദൈര്_ഘ്യം_മൂല്യം);
intptr_t 자료전문보내기(int അവസാനബിന്ദു, const void *ഡാറ്റാ, size_t 개수, int തിരഞ്ഞെടുക്കല്_മൂല്യം, const struct 통신주소 *ഇമെയിൽ, 통신주소길이형 ദൈര്_ഘ്യം_മൂല്യം);
intptr_t 자료전문받기(int അവസാനബിന്ദു, void *ഡാറ്റാ, size_t 개수, int തിരഞ്ഞെടുക്കല്_മൂല്യം, struct 통신주소 *ഇമെയിൽ, 통신주소길이형 *ദൈര്_ഘ്യം_മൂല്യം);
int 통신주소읽기(int അവസാനബിന്ദു, struct 통신주소 *ഇമെയിൽ, 통신주소길이형 *ദൈര്_ഘ്യം_മൂല്യം);
int കണക്റ്റ്_നെറ്റ്_വർക്ക്(int അവസാനബിന്ദു, const struct 통신주소 *ഇമെയിൽ, 통신주소길이형 ദൈര്_ഘ്യം_മൂല്യം);
int 통신연결기다리기(int അവസാനബിന്ദു, int 대기수);
int സ്വീകരിക്കുക_നെറ്റ്_വർക്ക്_കണക്ഷൻ(int അവസാനബിന്ദു, struct 통신주소 *ഇമെയിൽ, 통신주소길이형 *ദൈര്_ഘ്യം_മൂല്യം);

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
static inline uint16_t 망차례짧은수(uint16_t മൂല്യം) { return (uint16_t)((മൂല്യം >> 8) | (മൂല്യം << 8)); }
static inline uint32_t നെറ്റ്_വർക്ക്_പൂര്_ണ്ണസംഖ്യ(uint32_t മൂല്യം) { return ((മൂല്യം & 255u) << 24) | ((മൂല്യം & 0xff00u) << 8) | ((മൂല്യം >> 8) & 0xff00u) | (മൂല്യം >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t മൂല്യം) { return 망차례짧은수(മൂല്യം); }
static inline uint32_t മൊബൈൽ_ക്രമം_പൂര്_ണ്ണസംഖ്യ(uint32_t മൂല്യം) { return നെറ്റ്_വർക്ക്_പൂര്_ണ്ണസംഖ്യ(മൂല്യം); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return നെറ്റ്_വർക്ക്_പൂര്_ണ്ണസംഖ്യ(x); }
#endif
