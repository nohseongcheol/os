#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Ачуу open
#define Окуу read
#define Жазуу write
#define Жабуу close
#define seek lseek
#define sync fsync
#define Өчүрүү unlink
#define Туташуу connect
