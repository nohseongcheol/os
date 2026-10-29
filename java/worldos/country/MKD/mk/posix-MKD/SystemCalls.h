#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Отвори open
#define Читај read
#define Запиши write
#define Затвори close
#define seek lseek
#define sync fsync
#define Отстрани unlink
#define Врзи_се connect
