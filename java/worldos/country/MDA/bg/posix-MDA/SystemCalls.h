#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Отваряне open
#define Четене read
#define Писане write
#define Затворен close
#define seek lseek
#define sync fsync
#define Премахване unlink
#define Свързване connect
