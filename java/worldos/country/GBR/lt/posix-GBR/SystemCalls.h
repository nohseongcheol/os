#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Atverti open
#define Skaitymas read
#define Rašymas write
#define Užverti close
#define seek lseek
#define sync fsync
#define Šalinti unlink
#define Prisijungti connect
