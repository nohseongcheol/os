#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define විවෘත_කරන්න open
#define කියවීම read
#define ලිවීම write
#define වසන්න close
#define seek lseek
#define sync fsync
#define ඉවත්_කරන්න unlink
#define සම්බන්ද_වන්න connect
