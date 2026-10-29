#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define abrir open
#define leer read
#define escribir write
#define cerrar close
#define posicionar lseek
#define sincronizar fsync
#define eliminar unlink
#define conectar connect
