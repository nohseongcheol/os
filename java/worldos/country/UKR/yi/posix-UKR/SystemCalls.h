#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define עפֿן open
#define פֿאַרמאַך close
#define seek lseek
#define sync fsync
#define remove unlink
