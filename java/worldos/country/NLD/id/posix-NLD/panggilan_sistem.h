#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Buka open
#define Baca read
#define Tulis write
#define Tutup close
#define seek lseek
#define sync fsync
#define Hapus unlink
#define Sambung connect
