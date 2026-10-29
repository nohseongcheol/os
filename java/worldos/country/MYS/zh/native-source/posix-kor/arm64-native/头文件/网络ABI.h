#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "文件ABI.h"
/* 표준 ABI는 기존 可执行文件文件·外部值 코드와 연결할 때만 사용한다. */
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
 * 地址(住所)는 도착할 곳, 갈래는 地址 运行系统值, 数据报(電文)은 边界位置值 있는 通信 자료다. */
enum 网络常量 {
    互联网族 = 2, 流网络 = 1, 数据报套接字 = 2,
    流传输协议 = 6, 数据报协议 = 17,
    环回地址 = 0x7f000001u, 全部连接状态地址列 = 0, 尝试执行再次错误 = 11
};
typedef uint32_t 套接字地址长度类型;
struct 套接字地址 { uint16_t 地址族; unsigned char 地址数据[14]; };
struct 互联网地址值 { uint32_t 地址值; };
struct 互联网套接字地址 {
    uint16_t 地址族;
    uint16_t 端口编号;
    struct 互联网地址值 互联网地址;
    unsigned char 边距值[8];
};
typedef struct 套接字地址 套接字地址类型;
typedef struct 互联网套接字地址 互联网套接字地址类型;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 检查互联网套接字地址大小[(sizeof(struct 互联网套接字地址)==16)?1:-1];
typedef char 检查互联网套接字地址导航[(offsetof(struct 互联网套接字地址,互联网地址)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 创建端点(int 地址族, int 通信模式, int 传送协议);
int 绑定地址(int 端点, const struct 套接字地址 *地址, 套接字地址长度类型 长度);
intptr_t 发送数据报数据(int 端点, const void *数据, size_t 项目个数, int 选中状态值, const struct 套接字地址 *地址, 套接字地址长度类型 长度);
intptr_t 接收数据报数据(int 端点, void *数据, size_t 项目个数, int 选中状态值, struct 套接字地址 *地址, 套接字地址长度类型 *长度);
int 读取套接字地址(int 端点, struct 套接字地址 *地址, 套接字地址长度类型 *长度);
int 连接网络(int 端点, const struct 套接字地址 *地址, 套接字地址长度类型 长度);
int 等待状态用于网络连接状态(int 端点, int 等待中个数);
int 接受网络连接状态(int 端点, struct 套接字地址 *地址, 套接字地址长度类型 *长度);

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
static inline uint16_t 网络短整数(uint16_t 值) { return (uint16_t)((值 >> 8) | (值 << 8)); }
static inline uint32_t 网络整数(uint32_t 值) { return ((值 & 255u) << 24) | ((值 & 0xff00u) << 8) | ((值 >> 8) & 0xff00u) | (值 >> 24); }
static inline uint16_t 设备排序短整数(uint16_t 值) { return 网络短整数(值); }
static inline uint32_t 设备排序整数(uint32_t 值) { return 网络整数(值); }
static inline uint16_t pk_htons(uint16_t x) { return 网络短整数(x); }
static inline uint32_t pk_htonl(uint32_t x) { return 网络整数(x); }
#endif
