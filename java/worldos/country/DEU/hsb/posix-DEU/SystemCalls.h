#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Wočinić open
#define Čitać read
#define Pisać write
#define seek lseek
#define sync fsync
#define Zničić unlink
