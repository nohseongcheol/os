#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Obre open
#define Lectura read
#define Escriptura write
#define Tanca close
#define seek lseek
#define sync fsync
#define Suprimeix unlink
#define Connecta connect
