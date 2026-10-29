#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Ireki open
#define Irakurri read
#define Idatzi write
#define Itxi close
#define seek lseek
#define sync fsync
#define Kendu unlink
#define Konektatu connect
