#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define کھولیں open
#define پڑھیں read
#define لکھیں write
#define بند_کریں close
#define seek lseek
#define sync fsync
#define حذف_کریں unlink
#define متصل_ہوں connect
