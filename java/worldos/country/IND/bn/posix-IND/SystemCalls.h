#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define খুলুন open
#define পড়া read
#define লেখা write
#define বন্ধ_করুন close
#define seek lseek
#define sync fsync
#define মুছে_ফেলুন unlink
#define সংযোগ_স্থাপনা connect
