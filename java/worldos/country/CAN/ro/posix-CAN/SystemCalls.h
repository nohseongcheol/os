#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Deschide open
#define Citire read
#define Scriere write
#define Închide close
#define seek lseek
#define sync fsync
#define Elimină unlink
#define Conectează connect
