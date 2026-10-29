#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Opna open
#define Lestur read
#define Skrift write
#define Loka close
#define seek lseek
#define sync fsync
#define Fjarlægja unlink
#define Tengjast connect
