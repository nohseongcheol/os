#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Aç open
#define Okuma read
#define Yazma write
#define Kapat close
#define seek lseek
#define sync fsync
#define Kaldır unlink
#define Bağlan connect
