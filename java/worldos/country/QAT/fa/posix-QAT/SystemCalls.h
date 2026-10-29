#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define باز_کردن open
#define خواندن read
#define نوشتن write
#define بستن close
#define seek lseek
#define sync fsync
#define حذف unlink
#define اتصال connect
