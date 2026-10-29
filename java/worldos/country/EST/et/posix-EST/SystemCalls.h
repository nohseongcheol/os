#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Ava open
#define Lugemine read
#define Kirjutamine write
#define Suletud close
#define seek lseek
#define sync fsync
#define Eemalda unlink
#define Ühendu connect
