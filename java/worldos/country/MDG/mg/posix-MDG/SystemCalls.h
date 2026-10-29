#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Sokafy open
#define Mamaky read
#define Manoratra write
#define hidio close
#define seek lseek
#define sync fsync
#define Esory unlink
#define Atomboy connect
