#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define ખોલો open
#define વાંચો read
#define લખો write
#define બંધ_કરો close
#define seek lseek
#define sync fsync
#define દૂર_કરો unlink
#define સંપર્ક_કરો connect
