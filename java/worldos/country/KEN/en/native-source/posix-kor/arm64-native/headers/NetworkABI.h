#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "FileABI.h"
/* 표준 ABI는 기존 executableFile·externalValue 코드와 연결할 때만 사용한다. */
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

/* English 자료형은 macroValue 별칭이 아닌 독립된 구조체다.
 * address(住所)는 도착할 곳, 갈래는 address operatingSystemValue, datagram(電文)은 boundaryValue 있는 communication 자료다. */
enum networkConstant {
    InternetFamily = 2, StreamNetwork = 1, DatagramSocket = 2,
    streamTransportProtocol = 6, DatagramProtocol = 17,
    loopbackAddress = 0x7f000001u, allConnectionAddresses = 0, TryAgainError = 11
};
typedef uint32_t socketAddressLengthType;
struct SocketAddress { uint16_t addressFamily; unsigned char addressData[14]; };
struct internetAddressValue { uint32_t addressValue; };
struct InternetSocketAddress {
    uint16_t addressFamily;
    uint16_t portNumber;
    struct internetAddressValue InternetAddress;
    unsigned char marginValue[8];
};
typedef struct SocketAddress socketAddressType;
typedef struct InternetSocketAddress internetSocketAddressType;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char checkInternetSocketAddressSize[(sizeof(struct InternetSocketAddress)==16)?1:-1];
typedef char checkInternetSocketAddressLayout[(offsetof(struct InternetSocketAddress,InternetAddress)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int createEndpoint(int addressFamily, int communicationMode, int transferProtocol);
int bindAddress(int endpoint, const struct SocketAddress *address, socketAddressLengthType lengthValue);
intptr_t sendDatagramData(int endpoint, const void *data, size_t itemCount, int selectionValue, const struct SocketAddress *address, socketAddressLengthType lengthValue);
intptr_t receiveDatagramData(int endpoint, void *data, size_t itemCount, int selectionValue, struct SocketAddress *address, socketAddressLengthType *lengthValue);
int readSocketAddress(int endpoint, struct SocketAddress *address, socketAddressLengthType *lengthValue);
int connectNetwork(int endpoint, const struct SocketAddress *address, socketAddressLengthType lengthValue);
int waitForNetworkConnection(int endpoint, int waitingCount);
int acceptNetworkConnection(int endpoint, struct SocketAddress *address, socketAddressLengthType *lengthValue);

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
static inline uint16_t networkShort(uint16_t value) { return (uint16_t)((value >> 8) | (value << 8)); }
static inline uint32_t networkInteger(uint32_t value) { return ((value & 255u) << 24) | ((value & 0xff00u) << 8) | ((value >> 8) & 0xff00u) | (value >> 24); }
static inline uint16_t deviceOrderShort(uint16_t value) { return networkShort(value); }
static inline uint32_t deviceOrderInteger(uint32_t value) { return networkInteger(value); }
static inline uint16_t pk_htons(uint16_t x) { return networkShort(x); }
static inline uint32_t pk_htonl(uint32_t x) { return networkInteger(x); }
#endif
