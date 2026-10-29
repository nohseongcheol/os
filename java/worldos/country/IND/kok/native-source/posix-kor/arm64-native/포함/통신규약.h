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

/* 한국어 자료형은 मॅक्रो_मोल 별칭이 아닌 독립된 구조체다.
 * नामो(住所)는 도착할 곳, 갈래는 नामो ऑपरेटिंग_प्रणाली_मोल, 전문(電文)은 경계 있는 통신 자료다. */
enum नॅटवर्क_अचल {
    कूप_कुटुंब = 2, Stream_नॅटवर्क = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t नामो_कुटुंब; unsigned char नामो_डेटा[14]; };
struct माजाळ्याचो_नामो_मोल { uint32_t नामो_मोल; };
struct 인터넷통신주소 {
    uint16_t नामो_कुटुंब;
    uint16_t 접속번호;
    struct माजाळ्याचो_नामो_मोल माजाळ्याचो_नामो;
    unsigned char समास_मोल[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,माजाळ्याचो_नामो)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int नामो_कुटुंब, int 통신방식, int ट्रान्सफर_प्रोटोकॉल);
int BIND_नामो(int 종단, const struct 통신주소 *नामो, 통신주소길이형 लांबाय_मोल);
intptr_t 자료전문보내기(int 종단, const void *डेटा, size_t आयटम_COUNT, int निवड_मोल, const struct 통신주소 *नामो, 통신주소길이형 लांबाय_मोल);
intptr_t 자료전문받기(int 종단, void *डेटा, size_t आयटम_COUNT, int निवड_मोल, struct 통신주소 *नामो, 통신주소길이형 *लांबाय_मोल);
int 통신주소읽기(int 종단, struct 통신주소 *नामो, 통신주소길이형 *लांबाय_मोल);
int कनॅक्ट_नॅटवर्क(int 종단, const struct 통신주소 *नामो, 통신주소길이형 लांबाय_मोल);
int 통신연결기다리기(int 종단, int 대기수);
int स्विकारचें_नॅटवर्क_कनॅक्शन(int 종단, struct 통신주소 *नामो, 통신주소길이형 *लांबाय_मोल);

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
static inline uint16_t 망차례짧은수(uint16_t मोल) { return (uint16_t)((मोल >> 8) | (मोल << 8)); }
static inline uint32_t नॅटवर्क_पुर्णांक(uint32_t मोल) { return ((मोल & 255u) << 24) | ((मोल & 0xff00u) << 8) | ((मोल >> 8) & 0xff00u) | (मोल >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t मोल) { return 망차례짧은수(मोल); }
static inline uint32_t मोबायल_क्रम_पुर्णांक(uint32_t मोल) { return नॅटवर्क_पुर्णांक(मोल); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return नॅटवर्क_पुर्णांक(x); }
#endif
