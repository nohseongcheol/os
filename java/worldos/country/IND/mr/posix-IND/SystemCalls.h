#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define उघडा open
#define वाचन read
#define लेखन write
#define बंद_करा close
#define seek lseek
#define sync fsync
#define काढून_टाका unlink
#define जोडा connect
