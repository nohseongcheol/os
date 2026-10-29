#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Apri open
#define Lettura read
#define Scrittura write
#define Chiudi close
#define seek lseek
#define sync fsync
#define Rimuovi unlink
#define Connetti connect
