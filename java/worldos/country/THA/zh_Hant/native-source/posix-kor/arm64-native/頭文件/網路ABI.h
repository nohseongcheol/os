#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "檔案ABI.h"
/* 표준 ABI는 기존 可執行文件檔案·外部值 코드와 연결할 때만 사용한다. */
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

/* 中文 자료형은 宏值 별칭이 아닌 독립된 구조체다.
 * 地址(住所)는 도착할 곳, 갈래는 地址 運行系統值, 數據報(電文)은 邊界位置值 있는 通信 자료다. */
enum 網路常量 {
    互聯網族 = 2, 流網路 = 1, 數據報通訊端 = 2,
    流傳輸通訊協定 = 6, 數據報通訊協定 = 17,
    環回地址 = 0x7f000001u, 全部連接狀態地址列 = 0, 嘗試執行再次錯誤 = 11
};
typedef uint32_t 通訊端地址長度類型;
struct 通訊端地址 { uint16_t 地址族; unsigned char 地址資料[14]; };
struct 互聯網地址值 { uint32_t 地址值; };
struct 互聯網通訊端地址 {
    uint16_t 地址族;
    uint16_t 埠編號;
    struct 互聯網地址值 互聯網地址;
    unsigned char 邊距值[8];
};
typedef struct 通訊端地址 通訊端地址類型;
typedef struct 互聯網通訊端地址 互聯網通訊端地址類型;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 檢查互聯網通訊端地址大小[(sizeof(struct 互聯網通訊端地址)==16)?1:-1];
typedef char 檢查互聯網通訊端地址導航[(offsetof(struct 互聯網通訊端地址,互聯網地址)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 創建端點(int 地址族, int 通信模式, int 傳送通訊協定);
int 綁定地址(int 端點, const struct 通訊端地址 *地址, 通訊端地址長度類型 長度);
intptr_t 發送數據報資料(int 端點, const void *資料, size_t 項目個數, int 選中狀態值, const struct 通訊端地址 *地址, 通訊端地址長度類型 長度);
intptr_t 接收數據報資料(int 端點, void *資料, size_t 項目個數, int 選中狀態值, struct 通訊端地址 *地址, 通訊端地址長度類型 *長度);
int 讀取通訊端地址(int 端點, struct 通訊端地址 *地址, 通訊端地址長度類型 *長度);
int 連接網路(int 端點, const struct 通訊端地址 *地址, 通訊端地址長度類型 長度);
int 等待狀態用於網路連接狀態(int 端點, int 等待中個數);
int 接受網路連接狀態(int 端點, struct 通訊端地址 *地址, 通訊端地址長度類型 *長度);

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
static inline uint16_t 網路短整數(uint16_t 值) { return (uint16_t)((值 >> 8) | (值 << 8)); }
static inline uint32_t 網路整數(uint32_t 值) { return ((值 & 255u) << 24) | ((值 & 0xff00u) << 8) | ((值 >> 8) & 0xff00u) | (值 >> 24); }
static inline uint16_t 設備排序短整數(uint16_t 值) { return 網路短整數(值); }
static inline uint32_t 設備排序整數(uint32_t 值) { return 網路整數(值); }
static inline uint16_t pk_htons(uint16_t x) { return 網路短整數(x); }
static inline uint32_t pk_htonl(uint32_t x) { return 網路整數(x); }
#endif
