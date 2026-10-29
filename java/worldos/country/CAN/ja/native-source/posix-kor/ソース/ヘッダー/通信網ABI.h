#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 通信端点作成 socket
#define 番地結合 bind
#define データグラムデータ送信 sendto
#define データグラムデータ受取 recvfrom
#define ソケット番地読取 getsockname
#define 通信網設定値変更 setsockopt
#define 通信網番地解析 inet_pton
#define 書式通信網番地 inet_ntop
#define 通信網短整数 htons
#define 通信網整数値 htonl
#define 装置順序短整数 ntohs
#define 装置順序整数値 ntohl
#endif
