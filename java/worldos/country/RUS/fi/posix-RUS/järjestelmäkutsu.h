#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Avaa open
#define Luku read
#define Kirjoitus write
#define Sulje close
#define seek lseek
#define sync fsync
#define Poista unlink
#define Yhdistä connect
