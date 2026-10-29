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

/* Ikinyarwanda 자료형은 makoro_agaciro 별칭이 아닌 독립된 구조체다.
 * aderesi(住所)는 도착할 곳, 갈래는 aderesi sisitemu_ngengamikorere_agaciro, 전문(電文)은 경계 있는 통신 자료다. */
enum Urusobemiyoboro_kidahinduka {
    karawudi_Umuryango = 2, Stream_Urusobemiyoboro = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t aderesi_Umuryango; unsigned char aderesi_amakurushingiro[14]; };
struct Aderesi_ya_Interineti_agaciro { uint32_t aderesi_agaciro; };
struct 인터넷통신주소 {
    uint16_t aderesi_Umuryango;
    uint16_t 접속번호;
    struct Aderesi_ya_Interineti_agaciro Aderesi_ya_Interineti;
    unsigned char marije_agaciro[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Aderesi_ya_Interineti)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int aderesi_Umuryango, int 통신방식, int iyimura_porotokore);
int BIND_aderesi(int 종단, const struct 통신주소 *aderesi, 통신주소길이형 uburebure_agaciro);
intptr_t 자료전문보내기(int 종단, const void *amakurushingiro, size_t 개수, int ihitamo_agaciro, const struct 통신주소 *aderesi, 통신주소길이형 uburebure_agaciro);
intptr_t 자료전문받기(int 종단, void *amakurushingiro, size_t 개수, int ihitamo_agaciro, struct 통신주소 *aderesi, 통신주소길이형 *uburebure_agaciro);
int 통신주소읽기(int 종단, struct 통신주소 *aderesi, 통신주소길이형 *uburebure_agaciro);
int Guhuza_Urusobemiyoboro(int 종단, const struct 통신주소 *aderesi, 통신주소길이형 uburebure_agaciro);
int 통신연결기다리기(int 종단, int 대기수);
int kwemera_ukwihuza_ku_rusobemiyoboro(int 종단, struct 통신주소 *aderesi, 통신주소길이형 *uburebure_agaciro);

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
static inline uint16_t 망차례짧은수(uint16_t agaciro) { return (uint16_t)((agaciro >> 8) | (agaciro << 8)); }
static inline uint32_t Urusobemiyoboro_umubare_wuzuye(uint32_t agaciro) { return ((agaciro & 255u) << 24) | ((agaciro & 0xff00u) << 8) | ((agaciro >> 8) & 0xff00u) | (agaciro >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t agaciro) { return 망차례짧은수(agaciro); }
static inline uint32_t igendanwa_umujyo_umubare_wuzuye(uint32_t agaciro) { return Urusobemiyoboro_umubare_wuzuye(agaciro); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return Urusobemiyoboro_umubare_wuzuye(x); }
#endif
