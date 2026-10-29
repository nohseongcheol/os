#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define ליצור_משתתף socket
#define לאגד_למען bind
#define שלח_יחידת_נתונים_נתונים sendto
#define לקבל_יחידת_נתונים_נתונים recvfrom
#define 통신주소읽기 getsockname
#define שנה_רשת_הגדרות setsockopt
#define ניתוח_מבנה_טקסט_מזהה_רשת inet_pton
#define לעצב_מזהה_רשת inet_ntop
#define 망차례짧은수 htons
#define רשת_מספר_שלם htonl
#define 장치차례짧은수 ntohs
#define התקן_סדר_מספר_שלם ntohl
#endif
