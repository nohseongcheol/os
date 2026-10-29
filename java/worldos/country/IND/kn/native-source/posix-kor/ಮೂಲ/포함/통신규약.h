#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ಬೈಂಡ್_ಮಾಡು_ಇಮೇಲ್ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ಬದಲಿಸು_ನೆಟ್_ವರ್ಕ್_ಸೆಟ್ಟಿಂಗ್ಸ್ setsockopt
#define ಪಾರ್ಸ್_ಮಾಡಿ_ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್ inet_pton
#define ಸ್ವರೂಪ_ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್ inet_ntop
#define 망차례짧은수 htons
#define ನೆಟ್_ವರ್ಕ್_ಪೂರ್ಣಸಂಖ್ಯೆ htonl
#define 장치차례짧은수 ntohs
#define ಸಾಧನ_ಕ್ರಮ_ಪೂರ್ಣಸಂಖ್ಯೆ ntohl
#endif
