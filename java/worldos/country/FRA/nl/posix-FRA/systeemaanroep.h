#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Openen open
#define Lezen read
#define Schrijven write
#define Sluiten close
#define seek lseek
#define sync fsync
#define Verwijderen unlink
#define Verbinden connect
