#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define 열기 open
#define 읽기 read
#define 쓰기 write
#define 닫기 close
#define 위치옮기기 lseek
#define 기록맞추기 fsync
#define 지우기 unlink
#define 연결하기 connect
