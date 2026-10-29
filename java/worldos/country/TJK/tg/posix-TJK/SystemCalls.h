#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Хондан read
#define Навиштан write
#define Пӯшидан close
#define seek lseek
#define sync fsync
#define Нобуд_кардан unlink
