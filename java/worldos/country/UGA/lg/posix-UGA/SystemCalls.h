#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Bikkula open
#define Bikka close
#define seek lseek
#define sync fsync
#define Luggyemu unlink
