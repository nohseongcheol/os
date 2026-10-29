#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 निष्पादन_योग्य_फ़ाइल·बाहरी_मान 코드와 연결할 때만 사용한다. */
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

/* हिंदी 자료형은 मैक्रो_मान 별칭이 아닌 독립된 구조체다.
 * पता(住所)는 도착할 곳, 갈래는 पता ऑपरेटिंग_सिस्टम_मान, स्वतंत्रसंदेश(電文)은 경계 있는 통신 자료다. */
enum नेटवर्क_अचर {
    क्लाउड_समूह = 2, स्ट्रीम_नेटवर्क = 1, 전문통신 = 2,
    स्ट्रीम_ट्रांसपोर्ट_प्रोटोकॉल = 6, 전문전송규약 = 17,
    लूपबैक_पता = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct सॉकेट_पता { uint16_t पता_समूह; unsigned char पता_डेटा[14]; };
struct इंटरनेट_पता_मान { uint32_t पता_मान; };
struct क्लाउड_सॉकेट_पता {
    uint16_t पता_समूह;
    uint16_t पोर्ट_संख्या;
    struct इंटरनेट_पता_मान इंटरनेट_पता;
    unsigned char उपांत_मान[8];
};
typedef struct सॉकेट_पता सॉकेट_पता_लिखें;
typedef struct क्लाउड_सॉकेट_पता क्लाउड_सॉकेट_पता_लिखें;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char जाँचें_क्लाउड_सॉकेट_पता_आकार[(sizeof(struct क्लाउड_सॉकेट_पता)==16)?1:-1];
typedef char जाँचें_क्लाउड_सॉकेट_पता_लेआउट[(offsetof(struct क्लाउड_सॉकेट_पता,इंटरनेट_पता)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int बनाएँ_एंडपॉइंट(int पता_समूह, int 통신방식, int हस्तांतरण_प्रोटोकॉल);
int बाइंड_करें_पता(int एंडपॉइंट, const struct सॉकेट_पता *पता, 통신주소길이형 길이);
intptr_t 자료전문보내기(int एंडपॉइंट, const void *आँकड़े, size_t 개수, int चयन_मान, const struct सॉकेट_पता *पता, 통신주소길이형 길이);
intptr_t 자료전문받기(int एंडपॉइंट, void *आँकड़े, size_t 개수, int चयन_मान, struct सॉकेट_पता *पता, 통신주소길이형 *길이);
int पढें_सॉकेट_पता(int एंडपॉइंट, struct सॉकेट_पता *पता, 통신주소길이형 *길이);
int कनेक्ट_नेटवर्क(int एंडपॉइंट, const struct सॉकेट_पता *पता, 통신주소길이형 길이);
int 통신연결기다리기(int एंडपॉइंट, int 대기수);
int स्वीकार_करें_नेटवर्क_कनेक्शन(int एंडपॉइंट, struct सॉकेट_पता *पता, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t मान) { return (uint16_t)((मान >> 8) | (मान << 8)); }
static inline uint32_t नेटवर्क_पूर्णांक(uint32_t मान) { return ((मान & 255u) << 24) | ((मान & 0xff00u) << 8) | ((मान >> 8) & 0xff00u) | (मान >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t मान) { return 망차례짧은수(मान); }
static inline uint32_t उपकरण_क्रम_पूर्णांक(uint32_t मान) { return नेटवर्क_पूर्णांक(मान); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return नेटवर्क_पूर्णांक(x); }
#endif
