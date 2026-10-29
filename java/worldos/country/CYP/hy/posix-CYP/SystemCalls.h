#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Բաց open
#define Ընթերցում read
#define Գրել write
#define Փակ close
#define seek lseek
#define sync fsync
#define Հեռացնել unlink
#define Միացնել connect
