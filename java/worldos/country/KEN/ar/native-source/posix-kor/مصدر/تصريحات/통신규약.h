#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define فتح_المشارك socket
#define يربط_عنوان bind
#define يرسل_مخطط_بيانات_بيانات sendto
#define يستلم_مخطط_بيانات_بيانات recvfrom
#define يقرأ_مأخذ_التوصيل_عنوان getsockname
#define يغيّر_شبكة_إعدادات setsockopt
#define يوزّع_معرف_الشبكة inet_pton
#define ينسق_معرف_الشبكة inet_ntop
#define 망차례짧은수 htons
#define شبكة_عدد_صحيح htonl
#define 장치차례짧은수 ntohs
#define جهاز_أمر_عدد_صحيح ntohl
#endif
