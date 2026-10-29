#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define เปิด_ปลายทาง socket
#define ผูก_อีเมล bind
#define ส่ง_เดตาแกรม_ข้อมูล sendto
#define รับ_เดตาแกรม_ข้อมูล recvfrom
#define 통신주소읽기 getsockname
#define เปลี่ยนแปลง_เครือข่าย_การตั้งค่า setsockopt
#define แยกวิเคราะห์_รหัสเครือข่าย inet_pton
#define รูปแบบ_รหัสเครือข่าย inet_ntop
#define 망차례짧은수 htons
#define เครือข่าย_จํานวนเต็ม htonl
#define 장치차례짧은수 ntohs
#define อุปกรณ์_ลําดับ_จํานวนเต็ม ntohl
#endif
