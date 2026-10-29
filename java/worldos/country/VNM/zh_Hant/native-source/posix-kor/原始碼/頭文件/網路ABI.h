#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 創建端點 socket
#define 綁定地址 bind
#define 發送數據報資料 sendto
#define 接收數據報資料 recvfrom
#define 讀取通訊端地址 getsockname
#define 更改網路設置 setsockopt
#define 解析網路地址 inet_pton
#define 格式網路地址 inet_ntop
#define 網路短整數 htons
#define 網路整數 htonl
#define 設備排序短整數 ntohs
#define 設備排序整數 ntohl
#endif
