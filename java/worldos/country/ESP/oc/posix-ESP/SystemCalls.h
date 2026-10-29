#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Dobrir open
#define Lectura read
#define Escritura write
#define Tampar close
#define seek lseek
#define sync fsync
#define Suprimir unlink
#define Se_connectar connect
