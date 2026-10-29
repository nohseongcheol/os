#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Iepenje open
#define Lêze read
#define Skriuwe write
#define Slute close
#define seek lseek
#define sync fsync
#define Fuortsmite unlink
