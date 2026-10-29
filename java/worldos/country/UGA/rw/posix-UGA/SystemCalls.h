#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Gufungura open
#define Gufunga close
#define seek lseek
#define sync fsync
#define Gukuraho unlink
