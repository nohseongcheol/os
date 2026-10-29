#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 εκτελέσιμο·εξωτερικός_τιμή 코드와 연결할 때만 사용한다. */
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

/* ελληνικά 자료형은 μακροεντολή_τιμή 별칭이 아닌 독립된 구조체다.
 * διεύθυνση(住所)는 도착할 곳, 갈래는 διεύθυνση λειτουργικό_σύστημα_τιμή, αυτοδύναμο_πακέτο(電文)은 όριο_τιμή 있는 통신 자료다. */
enum δίκτυο_σταθερά {
    πλέγμα_παιδικά = 2, ροή_δίκτυο = 1, υποδοχή_αυτοδύναμου_πακέτου = 2,
    ροή_πρωτόκολλο_μεταφοράς = 6, αυτοδύναμο_πακέτο_πρωτόκολλο = 17,
    διεύθυνση_βρόχου_επιστροφής = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t υποδοχή_διεύθυνση_διάρκεια_Τύπος;
struct υποδοχή_διεύθυνση { uint16_t διεύθυνση_παιδικά; unsigned char διεύθυνση_δεδομένα[14]; };
struct διεύθυνση_Internet_τιμή { uint32_t διεύθυνση_τιμή; };
struct πλέγμα_υποδοχή_διεύθυνση {
    uint16_t διεύθυνση_παιδικά;
    uint16_t αριθμός_θύρας;
    struct διεύθυνση_Internet_τιμή διεύθυνση_Internet;
    unsigned char περιθώριο_τιμή[8];
};
typedef struct υποδοχή_διεύθυνση υποδοχή_διεύθυνση_Τύπος;
typedef struct πλέγμα_υποδοχή_διεύθυνση πλέγμα_υποδοχή_διεύθυνση_Τύπος;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char ελέγχω_πλέγμα_υποδοχή_διεύθυνση_αλλάζω_μέγεθος[(sizeof(struct πλέγμα_υποδοχή_διεύθυνση)==16)?1:-1];
typedef char ελέγχω_πλέγμα_υποδοχή_διεύθυνση_Διάταξη[(offsetof(struct πλέγμα_υποδοχή_διεύθυνση,διεύθυνση_Internet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int ανοίγω_τελικό_σημείο(int διεύθυνση_παιδικά, int 통신방식, int Μεταφορά_πρωτόκολλο);
int συνδέω_διεύθυνση(int τελικό_σημείο, const struct υποδοχή_διεύθυνση *διεύθυνση, υποδοχή_διεύθυνση_διάρκεια_Τύπος διάρκεια_τιμή);
intptr_t στέλνω_αυτοδύναμο_πακέτο_δεδομένα(int τελικό_σημείο, const void *δεδομένα, size_t 개수, int επιλογή_τιμή, const struct υποδοχή_διεύθυνση *διεύθυνση, υποδοχή_διεύθυνση_διάρκεια_Τύπος διάρκεια_τιμή);
intptr_t λαμβάνω_αυτοδύναμο_πακέτο_δεδομένα(int τελικό_σημείο, void *δεδομένα, size_t 개수, int επιλογή_τιμή, struct υποδοχή_διεύθυνση *διεύθυνση, υποδοχή_διεύθυνση_διάρκεια_Τύπος *διάρκεια_τιμή);
int 통신주소읽기(int τελικό_σημείο, struct υποδοχή_διεύθυνση *διεύθυνση, υποδοχή_διεύθυνση_διάρκεια_Τύπος *διάρκεια_τιμή);
int συνδέω_δίκτυο(int τελικό_σημείο, const struct υποδοχή_διεύθυνση *διεύθυνση, υποδοχή_διεύθυνση_διάρκεια_Τύπος διάρκεια_τιμή);
int 통신연결기다리기(int τελικό_σημείο, int 대기수);
int αποδέχομαι_σύνδεση_δικτύου(int τελικό_σημείο, struct υποδοχή_διεύθυνση *διεύθυνση, υποδοχή_διεύθυνση_διάρκεια_Τύπος *διάρκεια_τιμή);

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
static inline uint16_t 망차례짧은수(uint16_t τιμή) { return (uint16_t)((τιμή >> 8) | (τιμή << 8)); }
static inline uint32_t δίκτυο_ακέραιος(uint32_t τιμή) { return ((τιμή & 255u) << 24) | ((τιμή & 0xff00u) << 8) | ((τιμή >> 8) & 0xff00u) | (τιμή >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t τιμή) { return 망차례짧은수(τιμή); }
static inline uint32_t συσκευή_σειρά_ακέραιος(uint32_t τιμή) { return δίκτυο_ακέραιος(τιμή); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return δίκτυο_ακέραιος(x); }
#endif
