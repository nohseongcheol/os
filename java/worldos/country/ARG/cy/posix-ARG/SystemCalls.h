#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Agor open
#define Darllen read
#define Ysgrifennu write
#define Cau close
#define seek lseek
#define sync fsync
#define Tynnu unlink
