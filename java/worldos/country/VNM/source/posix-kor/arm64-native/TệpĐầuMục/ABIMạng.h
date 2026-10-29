#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "ABITệp.h"
/* 표준 ABI는 기존 tệpTệpThựcThi·giáTrịBênNgoài 코드와 연결할 때만 사용한다. */
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

/* tiếngViệt 자료형은 giáTrịVĩLệnh 별칭이 아닌 독립된 구조체다.
 * địaChỉ(住所)는 도착할 곳, 갈래는 địaChỉ giáTrịHệThốngĐiềuHành, điệnDữLiệu(電文)은 giáTrịRanhGiới 있는 TruyềnThông 자료다. */
enum hằngMạng {
    HọLiênMạng = 2, MạngLuồng = 1, ỔCắmMạngĐiệnDữLiệu = 2,
    giaoThứcVậnChuyểnLuồng = 6, GiaoThứcĐiệnDữLiệu = 17,
    địaChỉVòngVề = 0x7f000001u, cácĐịaChỉKếtNốiTấtCả = 0, LỗiLạiThửLàm = 11
};
typedef uint32_t kiểuĐộDàiĐịaChỉỔCắmMạng;
struct ĐịaChỉỔCắmMạng { uint16_t họĐịaChỉ; unsigned char dữLiệuĐịaChỉ[14]; };
struct giáTrịĐịaChỉLiênMạng { uint32_t giáTrịĐịaChỉ; };
struct ĐịaChỉỔCắmMạngLiênMạng {
    uint16_t họĐịaChỉ;
    uint16_t sốCổng;
    struct giáTrịĐịaChỉLiênMạng ĐịaChỉLiênMạng;
    unsigned char giáTrịLề[8];
};
typedef struct ĐịaChỉỔCắmMạng kiểuĐịaChỉỔCắmMạng;
typedef struct ĐịaChỉỔCắmMạngLiênMạng kiểuĐịaChỉỔCắmMạngLiênMạng;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char kiểmTraCỡĐịaChỉỔCắmMạngLiênMạng[(sizeof(struct ĐịaChỉỔCắmMạngLiênMạng)==16)?1:-1];
typedef char kiểmTraBốTríĐịaChỉỔCắmMạngLiênMạng[(offsetof(struct ĐịaChỉỔCắmMạngLiênMạng,ĐịaChỉLiênMạng)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int tạoĐiểmCuối(int họĐịaChỉ, int chếĐộTruyềnThông, int giaoThứcChuyểnGiao);
int ràngBuộcĐịaChỉ(int điểmCuối, const struct ĐịaChỉỔCắmMạng *địaChỉ, kiểuĐộDàiĐịaChỉỔCắmMạng độDài);
intptr_t gửiDữLiệuĐiệnDữLiệu(int điểmCuối, const void *DữLiệu, size_t sốLượngPhầnMục, int giáTrịViệcChọn, const struct ĐịaChỉỔCắmMạng *địaChỉ, kiểuĐộDàiĐịaChỉỔCắmMạng độDài);
intptr_t nhậnDữLiệuĐiệnDữLiệu(int điểmCuối, void *DữLiệu, size_t sốLượngPhầnMục, int giáTrịViệcChọn, struct ĐịaChỉỔCắmMạng *địaChỉ, kiểuĐộDàiĐịaChỉỔCắmMạng *độDài);
int đọcĐịaChỉỔCắmMạng(int điểmCuối, struct ĐịaChỉỔCắmMạng *địaChỉ, kiểuĐộDàiĐịaChỉỔCắmMạng *độDài);
int kếtNốiMạng(int điểmCuối, const struct ĐịaChỉỔCắmMạng *địaChỉ, kiểuĐộDàiĐịaChỉỔCắmMạng độDài);
int chờKếtNốiMạngCho(int điểmCuối, int sốLượngĐangĐợi);
int chấpNhậnKếtNốiMạng(int điểmCuối, struct ĐịaChỉỔCắmMạng *địaChỉ, kiểuĐộDàiĐịaChỉỔCắmMạng *độDài);

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
static inline uint16_t ngắnKiểuMạng(uint16_t giáTrị) { return (uint16_t)((giáTrị >> 8) | (giáTrị << 8)); }
static inline uint32_t sốNguyênMạng(uint32_t giáTrị) { return ((giáTrị & 255u) << 24) | ((giáTrị & 0xff00u) << 8) | ((giáTrị >> 8) & 0xff00u) | (giáTrị >> 24); }
static inline uint16_t ngắnKiểuThứTựThiếtBị(uint16_t giáTrị) { return ngắnKiểuMạng(giáTrị); }
static inline uint32_t sốNguyênThứTựThiếtBị(uint32_t giáTrị) { return sốNguyênMạng(giáTrị); }
static inline uint16_t pk_htons(uint16_t x) { return ngắnKiểuMạng(x); }
static inline uint32_t pk_htonl(uint32_t x) { return sốNguyênMạng(x); }
#endif
