#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Отвори open
#define Чита read
#define Пише write
#define Затворен close
#define seek lseek
#define sync fsync
#define Уклони unlink
#define Повежи_се connect
