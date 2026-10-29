#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Opmaken open
#define Lesen read
#define Schrieven write
#define Sluten close
#define seek lseek
#define sync fsync
#define Entfernen unlink
#define Verbinnen connect
