#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Lees read
#define Skryf write
#define Sluit close
#define seek lseek
#define sync fsync
#define Verwyder unlink
#define Koppel connect
