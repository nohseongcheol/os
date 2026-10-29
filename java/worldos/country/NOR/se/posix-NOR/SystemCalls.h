#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Raba open
#define Loga read
#define Čále write
#define Gidde close
#define seek lseek
#define sync fsync
#define Váldde_eret unlink
