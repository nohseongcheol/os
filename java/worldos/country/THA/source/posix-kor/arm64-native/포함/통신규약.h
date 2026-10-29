#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 แฟ้มปฏิบัติการ·ภายนอก_ค่า 코드와 연결할 때만 사용한다. */
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

/* ไทย 자료형은 แมโคร_ค่า 별칭이 아닌 독립된 구조체다.
 * อีเมล(住所)는 도착할 곳, 갈래는 อีเมล ระบบปฏิบัติการ_ค่า, เดตาแกรม(電文)은 경계 있는 통신 자료다. */
enum เครือข่าย_ค่าคงที่ {
    คลาวด์_กลุ่ม = 2, สตรีม_เครือข่าย = 1, เดตาแกรมซ็อกเก็ต = 2,
    สตรีม_โพรโทคอลการส่งผ่าน = 6, เดตาแกรม_โพรโทคอล = 17,
    ที่อยู่ย้อนกลับ = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t อีเมล_กลุ่ม; unsigned char อีเมล_ข้อมูล[14]; };
struct ที่อยู่อินเทอร์เน็ต_ค่า { uint32_t อีเมล_ค่า; };
struct 인터넷통신주소 {
    uint16_t อีเมล_กลุ่ม;
    uint16_t หมายเลขพอร์ต;
    struct ที่อยู่อินเทอร์เน็ต_ค่า ที่อยู่อินเทอร์เน็ต;
    unsigned char ระยะขอบ_ค่า[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,ที่อยู่อินเทอร์เน็ต)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int เปิด_ปลายทาง(int อีเมล_กลุ่ม, int 통신방식, int โอน_โพรโทคอล);
int ผูก_อีเมล(int ปลายทาง, const struct 통신주소 *อีเมล, 통신주소길이형 길이);
intptr_t ส่ง_เดตาแกรม_ข้อมูล(int ปลายทาง, const void *ข้อมูล, size_t 개수, int การเลือก_ค่า, const struct 통신주소 *อีเมล, 통신주소길이형 길이);
intptr_t รับ_เดตาแกรม_ข้อมูล(int ปลายทาง, void *ข้อมูล, size_t 개수, int การเลือก_ค่า, struct 통신주소 *อีเมล, 통신주소길이형 *길이);
int 통신주소읽기(int ปลายทาง, struct 통신주소 *อีเมล, 통신주소길이형 *길이);
int เชื่อมต่อ_เครือข่าย(int ปลายทาง, const struct 통신주소 *อีเมล, 통신주소길이형 길이);
int 통신연결기다리기(int ปลายทาง, int 대기수);
int ยอมรับ_การเชื่อมต่อเครือข่าย(int ปลายทาง, struct 통신주소 *อีเมล, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t ค่า) { return (uint16_t)((ค่า >> 8) | (ค่า << 8)); }
static inline uint32_t เครือข่าย_จํานวนเต็ม(uint32_t ค่า) { return ((ค่า & 255u) << 24) | ((ค่า & 0xff00u) << 8) | ((ค่า >> 8) & 0xff00u) | (ค่า >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t ค่า) { return 망차례짧은수(ค่า); }
static inline uint32_t อุปกรณ์_ลําดับ_จํานวนเต็ม(uint32_t ค่า) { return เครือข่าย_จํานวนเต็ม(ค่า); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return เครือข่าย_จํานวนเต็ม(x); }
#endif
