#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define खोल्नुहोस् open
#define पढनुहोस् read
#define लेख्नुहोस् write
#define बन्दगर्नुहोस् close
#define seek lseek
#define sync fsync
#define हटाउने unlink
#define जडान connect
