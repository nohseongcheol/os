#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Atvērt open
#define Lasīt read
#define Rakstīt write
#define Aizvērt close
#define seek lseek
#define sync fsync
#define Aizvākt unlink
#define Savienoties connect
