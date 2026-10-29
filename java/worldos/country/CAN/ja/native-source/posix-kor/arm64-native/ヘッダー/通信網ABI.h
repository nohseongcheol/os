#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "ファイルABI.h"
/* 표준 ABI는 기존 実行形式ファイル·外部値 코드와 연결할 때만 사용한다. */
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

/* 日本語 자료형은 マクロ値 별칭이 아닌 독립된 구조체다.
 * 番地(番地)는 도착할 곳, 갈래는 番地 稼働システム値, データグラム(電文)은 境界位置値 있는 通信 자료다. */
enum 通信網定数 {
    インターネット体系 = 2, ストリーム通信網 = 1, データグラムソケット = 2,
    ストリーム輸送通信規約 = 6, データグラム通信規約 = 17,
    折返し番地 = 0x7f000001u, 全体接続状態番地一覧 = 0, 試行処理再試行エラー = 11
};
typedef uint32_t ソケット番地長さ型;
struct ソケット番地 { uint16_t 番地体系; unsigned char 番地データ[14]; };
struct インターネット番地値 { uint32_t 番地値; };
struct インターネットソケット番地 {
    uint16_t 番地体系;
    uint16_t ポート番号;
    struct インターネット番地値 インターネット番地;
    unsigned char 余白値[8];
};
typedef struct ソケット番地 ソケット番地型;
typedef struct インターネットソケット番地 インターネットソケット番地型;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char インターネットソケット番地容量検査[(sizeof(struct インターネットソケット番地)==16)?1:-1];
typedef char インターネットソケット番地配置検査[(offsetof(struct インターネットソケット番地,インターネット番地)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 通信端点作成(int 番地体系, int 通信方式, int 転送通信規約);
int 番地結合(int 通信端点, const struct ソケット番地 *番地, ソケット番地長さ型 長さ);
intptr_t データグラムデータ送信(int 通信端点, const void *データ, size_t 項目個数, int 選択状態値, const struct ソケット番地 *番地, ソケット番地長さ型 長さ);
intptr_t データグラムデータ受取(int 通信端点, void *データ, size_t 項目個数, int 選択状態値, struct ソケット番地 *番地, ソケット番地長さ型 *長さ);
int ソケット番地読取(int 通信端点, struct ソケット番地 *番地, ソケット番地長さ型 *長さ);
int 通信網接続(int 通信端点, const struct ソケット番地 *番地, ソケット番地長さ型 長さ);
int 対象通信網接続状態待合(int 通信端点, int 待機中個数);
int 通信網接続状態受理(int 通信端点, struct ソケット番地 *番地, ソケット番地長さ型 *長さ);

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
static inline uint16_t 通信網短整数(uint16_t 値) { return (uint16_t)((値 >> 8) | (値 << 8)); }
static inline uint32_t 通信網整数値(uint32_t 値) { return ((値 & 255u) << 24) | ((値 & 0xff00u) << 8) | ((値 >> 8) & 0xff00u) | (値 >> 24); }
static inline uint16_t 装置順序短整数(uint16_t 値) { return 通信網短整数(値); }
static inline uint32_t 装置順序整数値(uint32_t 値) { return 通信網整数値(値); }
static inline uint16_t pk_htons(uint16_t x) { return 通信網短整数(x); }
static inline uint32_t pk_htonl(uint32_t x) { return 通信網整数値(x); }
#endif
