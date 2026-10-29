#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ਜ਼ਿਲਦਬੰਦੀ_ਪਤਾ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ਬਦਲੋ_ਨੈਟਵਰਕ_ਸੈਟਿੰਗਾਂ setsockopt
#define ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਨੈਟਵਰਕ_ਪਤਾ inet_pton
#define ਸਰੂਪ_ਨੈਟਵਰਕ_ਪਤਾ inet_ntop
#define 망차례짧은수 htons
#define ਨੈਟਵਰਕ_ਪੂਰਣ_ਅੰਕ htonl
#define 장치차례짧은수 ntohs
#define ਤਜਵੀਜ_ਕ੍ਰਮ_ਪੂਰਣ_ਅੰਕ ntohl
#endif
