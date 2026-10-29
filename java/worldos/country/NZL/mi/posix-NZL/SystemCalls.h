#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Huaki open
#define Pānuitia read
#define Tuhia write
#define Kati close
#define seek lseek
#define sync fsync
#define Tangohia unlink
