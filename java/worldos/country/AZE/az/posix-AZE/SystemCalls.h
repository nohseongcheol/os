#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Aç open
#define Oxuma read
#define Yazma write
#define Bağla close
#define seek lseek
#define sync fsync
#define Çıxart unlink
#define Bağlan connect
