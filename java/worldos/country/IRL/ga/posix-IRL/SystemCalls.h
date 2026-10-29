#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Oscail open
#define Léigh read
#define Scríobh write
#define Dún close
#define seek lseek
#define sync fsync
#define Bain unlink
#define Nasc connect
