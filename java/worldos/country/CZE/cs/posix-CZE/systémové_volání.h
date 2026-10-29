#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Otevřít open
#define Čtení read
#define Zápis write
#define Zavřené close
#define seek lseek
#define sync fsync
#define Odstranit unlink
#define Připojit connect
