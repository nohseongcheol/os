#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Aç open
#define Oka read
#define Ýaz write
#define Ýap close
#define seek lseek
#define sync fsync
#define Çykar unlink
