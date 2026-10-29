#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define فتح open
#define قراءة read
#define كتابة write
#define إغلاق close
#define نقلالموضع lseek
#define مزامنة fsync
#define إزالة unlink
#define اتصال connect
