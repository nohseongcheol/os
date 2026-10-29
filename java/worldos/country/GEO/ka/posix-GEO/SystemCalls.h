#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define გახსნა open
#define კითხვა read
#define ჩაწერა write
#define დახურვა close
#define seek lseek
#define sync fsync
#define წაშლა unlink
#define დაკავშირება connect
