#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Hap open
#define Leximi read
#define Shkrimi write
#define Mbyll close
#define seek lseek
#define sync fsync
#define Hiq unlink
#define Lidhu connect
