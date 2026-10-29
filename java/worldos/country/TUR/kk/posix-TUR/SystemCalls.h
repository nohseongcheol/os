#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Ашу open
#define Оқу read
#define Жазу write
#define Жабу close
#define seek lseek
#define sync fsync
#define Өшіру unlink
#define Байланысу connect
