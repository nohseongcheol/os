#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Åbn open
#define Læse read
#define Skrive write
#define Luk close
#define seek lseek
#define sync fsync
#define Fjern unlink
#define Tilslut connect
