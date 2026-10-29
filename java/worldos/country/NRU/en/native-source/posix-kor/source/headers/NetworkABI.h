#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define createEndpoint socket
#define bindAddress bind
#define sendDatagramData sendto
#define receiveDatagramData recvfrom
#define readSocketAddress getsockname
#define changeNetworkSettings setsockopt
#define parseNetworkAddress inet_pton
#define formatNetworkAddress inet_ntop
#define networkShort htons
#define networkInteger htonl
#define deviceOrderShort ntohs
#define deviceOrderInteger ntohl
#endif
