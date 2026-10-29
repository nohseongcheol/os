#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Ochish open
#define Oʻqish read
#define Yozish write
#define Yopish close
#define seek lseek
#define sync fsync
#define Olib_tashlash unlink
#define Ulanish connect
