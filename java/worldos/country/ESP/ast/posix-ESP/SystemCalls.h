#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Abrir open
#define Llectura read
#define Escritura write
#define Zarrar close
#define seek lseek
#define sync fsync
#define Desaniciar unlink
#define Coneutar connect
