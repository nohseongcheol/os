#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Drovi open
#define Lére read
#define Sicrire write
#define Clôre close
#define seek lseek
#define sync fsync
#define Oister unlink
#define Raloyî connect
