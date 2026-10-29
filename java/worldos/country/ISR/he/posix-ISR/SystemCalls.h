#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define פתח open
#define קרא read
#define כתוב write
#define סגירה close
#define seek lseek
#define sync fsync
#define הסר unlink
#define חיבור connect
