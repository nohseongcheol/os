#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define खोलू open
#define पढ़ू read
#define लिखू write
#define बन्न_करू close
#define seek lseek
#define sync fsync
#define हटाबू unlink
#define जुड़ू connect
