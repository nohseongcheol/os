#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Odpri open
#define Branje read
#define Pisanje write
#define Zapri close
#define seek lseek
#define sync fsync
#define Odstrani unlink
#define Poveži connect
