#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Abrir open
#define Leitura read
#define Escrita write
#define Fechar close
#define seek lseek
#define sync fsync
#define Remover unlink
#define Ligar connect
