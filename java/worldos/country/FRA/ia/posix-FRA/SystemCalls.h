#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Aperir open
#define Lege read
#define Scribe write
#define Clauder close
#define seek lseek
#define sync fsync
#define Remover unlink
