#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Digeriñ open
#define Lenn read
#define Skrivañ write
#define Serriñ close
#define seek lseek
#define sync fsync
#define Dilemel unlink
#define Kennaskañ connect
