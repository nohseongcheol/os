#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "संचिका_द्विमानजोडणी.h"
/* 표준 ABI는 기존 निष्पादनीय_संचिका·बाह्य_मूल्य 코드와 연결할 때만 사용한다. */
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

/* मराठी 자료형은 मॅक्रो_मूल्य 별칭이 아닌 독립된 구조체다.
 * पत्ता(住所)는 도착할 곳, 갈래는 पत्ता ऑपरेटिंग_सिस्टम_मूल्य, स्वतंत्रसंदेश(電文)은 सीमा_मूल्य 있는 संचार 자료다. */
enum संचारजाळे_स्थिरांक {
    क्लाउड_कुटुंब = 2, प्रवाह_संचारजाळे = 1, स्वतंत्रसंदेश_संचारद्वार = 2,
    प्रवाह_वाहतूक_प्रोटोकॉल = 6, स्वतंत्रसंदेश_प्रोटोकॉल = 17,
    स्वपरतावा_पत्ता = 0x7f000001u, सर्व_कनेक्शन_पत्ते = 0, प्रयत्नकरा_पुन्हा_त्रुटी = 11
};
typedef uint32_t संचारद्वार_पत्ता_लांबी_टाइप_करा;
struct संचारद्वार_पत्ता { uint16_t पत्ता_कुटुंब; unsigned char पत्ता_डेटा[14]; };
struct इंटरनेट_पत्ता_मूल्य { uint32_t पत्ता_मूल्य; };
struct क्लाउड_संचारद्वार_पत्ता {
    uint16_t पत्ता_कुटुंब;
    uint16_t पोर्ट_नंबर;
    struct इंटरनेट_पत्ता_मूल्य इंटरनेट_पत्ता;
    unsigned char समास_मूल्य[8];
};
typedef struct संचारद्वार_पत्ता संचारद्वार_पत्ता_टाइप_करा;
typedef struct क्लाउड_संचारद्वार_पत्ता क्लाउड_संचारद्वार_पत्ता_टाइप_करा;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char क्लाउड_संचारद्वार_पत्ता_आकारा_तपासा[(sizeof(struct क्लाउड_संचारद्वार_पत्ता)==16)?1:-1];
typedef char क्लाउड_संचारद्वार_पत्ता_लेआउट_तपासा[(offsetof(struct क्लाउड_संचारद्वार_पत्ता,इंटरनेट_पत्ता)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int संचारटोक_तयार_करा(int पत्ता_कुटुंब, int संचार_मोड, int स्थानांतर_प्रोटोकॉल);
int बाइंड_करा_पत्ता(int संचारटोक, const struct संचारद्वार_पत्ता *पत्ता, संचारद्वार_पत्ता_लांबी_टाइप_करा लांबी_मूल्य);
intptr_t स्वतंत्रसंदेश_डेटा_पाठवा(int संचारटोक, const void *डेटा, size_t आयटम_संख्या, int निवड_मूल्य, const struct संचारद्वार_पत्ता *पत्ता, संचारद्वार_पत्ता_लांबी_टाइप_करा लांबी_मूल्य);
intptr_t स्वतंत्रसंदेश_डेटा_स्वीकारा(int संचारटोक, void *डेटा, size_t आयटम_संख्या, int निवड_मूल्य, struct संचारद्वार_पत्ता *पत्ता, संचारद्वार_पत्ता_लांबी_टाइप_करा *लांबी_मूल्य);
int संचारद्वार_पत्ता_वाचा(int संचारटोक, struct संचारद्वार_पत्ता *पत्ता, संचारद्वार_पत्ता_लांबी_टाइप_करा *लांबी_मूल्य);
int कनेक्ट_संचारजाळे(int संचारटोक, const struct संचारद्वार_पत्ता *पत्ता, संचारद्वार_पत्ता_लांबी_टाइप_करा लांबी_मूल्य);
int प्रतीक्षा_करा_साठी_नेटवर्क_कनेक्शन(int संचारटोक, int प्रतीक्षारत_संख्या);
int स्वीकारा_नेटवर्क_कनेक्शन(int संचारटोक, struct संचारद्वार_पत्ता *पत्ता, संचारद्वार_पत्ता_लांबी_टाइप_करा *लांबी_मूल्य);

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
static inline uint16_t संचारजाळे_लघु(uint16_t मूल्य) { return (uint16_t)((मूल्य >> 8) | (मूल्य << 8)); }
static inline uint32_t संचारजाळे_पूर्णांक(uint32_t मूल्य) { return ((मूल्य & 255u) << 24) | ((मूल्य & 0xff00u) << 8) | ((मूल्य >> 8) & 0xff00u) | (मूल्य >> 24); }
static inline uint16_t मोबाइल_क्रम_लघु(uint16_t मूल्य) { return संचारजाळे_लघु(मूल्य); }
static inline uint32_t मोबाइल_क्रम_पूर्णांक(uint32_t मूल्य) { return संचारजाळे_पूर्णांक(मूल्य); }
static inline uint16_t pk_htons(uint16_t x) { return संचारजाळे_लघु(x); }
static inline uint32_t pk_htonl(uint32_t x) { return संचारजाळे_पूर्णांक(x); }
#endif
