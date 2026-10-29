#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Otvoriť open
#define Čítanie read
#define Zápis write
#define Zatvoriť close
#define seek lseek
#define sync fsync
#define Odstrániť unlink
#define Pripojiť connect
