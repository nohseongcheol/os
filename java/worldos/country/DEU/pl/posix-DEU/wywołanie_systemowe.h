#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Otwórz open
#define Odczyt read
#define Zapis write
#define Zamknięte close
#define seek lseek
#define sync fsync
#define Usuń unlink
#define Połącz connect
