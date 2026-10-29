#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Abrir open
#define Lectura read
#define Escritura write
#define Pechar close
#define seek lseek
#define sync fsync
#define Retirar unlink
#define Conectar connect
