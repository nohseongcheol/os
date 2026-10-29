#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·חיצוני_ערך 코드와 연결할 때만 사용한다. */
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

/* עברית 자료형은 מאקרו_ערך 별칭이 아닌 독립된 구조체다.
 * למען(住所)는 도착할 곳, 갈래는 למען מערכת_הפעלה_ערך, יחידת_נתונים(電文)은 경계 있는 통신 자료다. */
enum רשת_קבוע {
    ענן_משפחה = 2, זרם_רשת = 1, Socket_של_יחידת_נתונים = 2,
    זרם_פרוטוקול_תעבורה = 6, יחידת_נתונים_פרוטוקול = 17,
    כתובת_לולאה_חוזרת = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t למען_משפחה; unsigned char למען_נתונים[14]; };
struct כתובת_אינטרנט_ערך { uint32_t למען_ערך; };
struct 인터넷통신주소 {
    uint16_t למען_משפחה;
    uint16_t מספר_יציאה;
    struct כתובת_אינטרנט_ערך כתובת_אינטרנט;
    unsigned char שוליים_ערך[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,כתובת_אינטרנט)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int ליצור_משתתף(int למען_משפחה, int 통신방식, int העבר_פרוטוקול);
int לאגד_למען(int משתתף, const struct 통신주소 *למען, 통신주소길이형 길이);
intptr_t שלח_יחידת_נתונים_נתונים(int משתתף, const void *נתונים, size_t 개수, int קטע_נבחר_ערך, const struct 통신주소 *למען, 통신주소길이형 길이);
intptr_t לקבל_יחידת_נתונים_נתונים(int משתתף, void *נתונים, size_t 개수, int קטע_נבחר_ערך, struct 통신주소 *למען, 통신주소길이형 *길이);
int 통신주소읽기(int משתתף, struct 통신주소 *למען, 통신주소길이형 *길이);
int לקשר_רשת(int משתתף, const struct 통신주소 *למען, 통신주소길이형 길이);
int 통신연결기다리기(int משתתף, int 대기수);
int לקבל_חיבור_רשת(int משתתף, struct 통신주소 *למען, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t ערך) { return (uint16_t)((ערך >> 8) | (ערך << 8)); }
static inline uint32_t רשת_מספר_שלם(uint32_t ערך) { return ((ערך & 255u) << 24) | ((ערך & 0xff00u) << 8) | ((ערך >> 8) & 0xff00u) | (ערך >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t ערך) { return 망차례짧은수(ערך); }
static inline uint32_t התקן_סדר_מספר_שלם(uint32_t ערך) { return רשת_מספר_שלם(ערך); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return רשת_מספר_שלם(x); }
#endif
