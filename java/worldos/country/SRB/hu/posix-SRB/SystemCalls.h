#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Megnyitás open
#define Olvasás read
#define Írás write
#define Bezárás close
#define seek lseek
#define sync fsync
#define Eltávolítás unlink
#define Kapcsolódás connect
