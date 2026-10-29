#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define খোলো open
#define পড়া read
#define লিখা write
#define বন্ধ_কৰক close
#define seek lseek
#define sync fsync
#define আঁতৰাওঁক unlink
#define সংযোগ_স্থাপনা connect
